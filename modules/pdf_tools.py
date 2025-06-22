from pdf2docx import Converter
import streamlit as st
import tempfile

def convert_pdf_word(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        cv = Converter(tmp_path)
        cv.convert("converted.docx", start=0, end=None)
        cv.close()
        st.success("PDF converted to Word successfully.")
        with open("converted.docx", "rb") as f:
            st.download_button("Download Word File", f, file_name="converted.docx")
    except Exception as e:
        st.error(f"Conversion failed: {e}")
        from pdf2docx import Converter

def convert_pdf_word(input_pdf, output_docx="converted.docx"):
    cv = Converter(input_pdf)
    cv.convert(output_docx, start=0, end=None)
    cv.close()
