import streamlit as st
import os
import tempfile

from modules import word_tools, pdf_tools, ppt_tools, image_tools, audio_tools, excel_tools
from utils.logger import log_event
from utils.helpers import get_file_extension, is_conversion_supported, save_uploaded_file

# --- App Config ---
st.set_page_config(page_title="AI File Converter", layout="wide")
st.title("🛠️ AI File Converter")
st.caption("Convert files between formats using AI-based tools.")

# --- Sidebar Info ---
with st.sidebar:
    st.markdown("## 📄 Supported Formats")
    st.markdown("- **Upload:** PDF, DOCX, PPTX, XLSX, XLS, JPG, JPEG, PNG, MP3, WAV")
    st.markdown("- **Convert To:** PDF, DOCX, PPTX, XLSX, MP3, WAV, JPG, PNG")
    st.markdown("💡 You can convert any supported file into any other format — your choice!")

# --- Config ---
SUPPORTED_INPUT_FORMATS = ["pdf", "docx", "pptx", "xlsx", "xls", "jpg", "jpeg", "png", "mp3", "wav"]
TARGET_FORMATS = ["PDF", "DOCX", "PPTX", "XLSX", "MP3", "WAV", "JPG", "PNG"]

# --- File Upload ---
uploaded_file = st.file_uploader("Upload a file to convert", type=SUPPORTED_INPUT_FORMATS)
target_format = st.selectbox("Choose format to convert to", TARGET_FORMATS)

if uploaded_file and target_format:
    file_name = uploaded_file.name
    source_ext = get_file_extension(file_name)
    target_ext = target_format.lower()

    st.write(f"📁 Uploaded file: `{file_name}`")

    if not is_conversion_supported(source_ext, target_ext):
        st.warning(f"⚠️ Conversion from `{source_ext.upper()}` to `{target_ext.upper()}` is not supported.")
    else:
        try:
            with st.spinner("🔄 Converting..."):
                tmp_file_path = save_uploaded_file(uploaded_file)

                output_file = None
                # Dispatch based on file type
                if source_ext in ["docx"]:
                    output_file = word_tools.convert_word(tmp_file_path, target_ext)
                elif source_ext == "pdf":
                    output_file = pdf_tools.convert_pdf(tmp_file_path, target_ext)
                elif source_ext in ["pptx"]:
                    output_file = ppt_tools.convert_ppt(tmp_file_path, target_ext)
                elif source_ext in ["jpg", "jpeg", "png"]:
                    output_file = image_tools.convert_image(tmp_file_path, target_ext)
                elif source_ext in ["mp3", "wav"]:
                    output_file = audio_tools.convert_audio(tmp_file_path, target_ext)
                elif source_ext in ["xlsx", "xls"]:
                    output_file = excel_tools.convert_excel(tmp_file_path, target_ext)

                if output_file and os.path.exists(output_file):
                    st.success("✅ Conversion successful!")
                    with open(output_file, "rb") as f:
                        st.download_button(
                            label=f"📥 Download converted.{target_ext}",
                            data=f,
                            file_name=f"converted.{target_ext}"
                        )
                else:
                    st.error("❌ Conversion failed: Output file was not generated.")

                log_event(f"Conversion used: {source_ext} → {target_ext} on file {file_name}")

        except Exception as e:
            st.error(f"❌ Conversion failed: {str(e)}")
