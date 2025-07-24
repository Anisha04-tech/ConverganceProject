from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from pdf2image import convert_from_path
import pytesseract
from fpdf import FPDF

app = Flask(__name__)

UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/pdf/merge', methods=['POST'])
def merge_pdfs():
    files = request.files.getlist('files')
    if not files or len(files) < 2:
        return jsonify({'error': 'At least two PDF files are required.'}), 400
    merger = PdfMerger()
    temp_files = []
    try:
        for file in files:
            filename = secure_filename(file.filename)
            temp_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(temp_path)
            temp_files.append(temp_path)
            merger.append(temp_path)
        output_path = os.path.join(UPLOAD_FOLDER, 'merged.pdf')
        merger.write(output_path)
        merger.close()
        return send_file(output_path, as_attachment=True, download_name='merged.pdf')
    finally:
        for f in temp_files:
            if os.path.exists(f):
                os.remove(f)

@app.route('/api/pdf/split', methods=['POST'])
def split_pdf():
    file = request.files.get('file')
    start = int(request.form.get('start', 1))
    end = int(request.form.get('end', 1))
    if not file:
        return jsonify({'error': 'PDF file is required.'}), 400
    filename = secure_filename(file.filename)
    temp_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(temp_path)
    reader = PdfReader(temp_path)
    writer = PdfWriter()
    for i in range(start-1, min(end, len(reader.pages))):
        writer.add_page(reader.pages[i])
    output_path = os.path.join(UPLOAD_FOLDER, 'split.pdf')
    with open(output_path, 'wb') as f:
        writer.write(f)
    os.remove(temp_path)
    return send_file(output_path, as_attachment=True, download_name='split.pdf')

@app.route('/api/pdf/ocr', methods=['POST'])
def ocr_pdf():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'PDF file is required.'}), 400
    filename = secure_filename(file.filename)
    temp_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(temp_path)
    # Convert PDF pages to images
    images = convert_from_path(temp_path)
    text_pages = []
    for img in images:
        text = pytesseract.image_to_string(img)
        text_pages.append(text)
    # Create a searchable PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    for page_text in text_pages:
        pdf.add_page()
        pdf.set_font('Arial', size=12)
        for line in page_text.split('\n'):
            pdf.cell(0, 10, line, ln=1)
    output_path = os.path.join(UPLOAD_FOLDER, 'ocr_output.pdf')
    pdf.output(output_path)
    os.remove(temp_path)
    return send_file(output_path, as_attachment=True, download_name='ocr_output.pdf')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)