from docx import Document
from fpdf import FPDF
import tempfile
import streamlit as st

def docx_to_pdf(uploaded_file):
    try:
        doc = Document(uploaded_file)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        for para in doc.paragraphs:
            pdf.multi_cell(0, 10, para.text)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            pdf.output(tmp.name)
            st.success("DOCX converted to PDF successfully.")
            with open(tmp.name, "rb") as f:
                st.download_button("Download PDF", f, file_name="converted.pdf")
    except Exception as e:
        st.error(f"DOCX conversion failed: {e}")