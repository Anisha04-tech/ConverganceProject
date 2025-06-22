from PIL import Image
import streamlit as st
import tempfile

def image_to_pdf(uploaded_file):
    try:
        image = Image.open(uploaded_file).convert("RGB")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            image.save(tmp.name, "PDF")
            st.success("Image converted to PDF successfully.")
            with open(tmp.name, "rb") as f:
                st.download_button("Download PDF", f, file_name="converted.pdf")
    except Exception as e:
        st.error(f"Image conversion failed: {e}")
        from PIL import Image
import os

def convert_image(image_path, output_format='PDF'):
    img = Image.open(image_path).convert("RGB")
    output_file = f"converted.{output_format.lower()}"
    img.save(output_file)
    return output_file
