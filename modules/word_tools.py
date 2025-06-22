from docx import Document
from pdf2docx import Converter

def convert_word_pdf(input_path, output_path):
    from docx2pdf import convert
    convert(input_path, output_path)
