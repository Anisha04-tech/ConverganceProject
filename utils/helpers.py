import os

def get_file_extension(filename):
    return filename.split('.')[-1].lower()

def is_conversion_supported(source_ext, target_ext):
    supported = {
        "pdf": ["docx", "pptx", "jpg", "png"],
        "docx": ["pdf", "jpg"],
        "pptx": ["pdf", "jpg"],
        "xlsx": ["pdf"],
        "xls": ["pdf"],
        "jpg": ["pdf", "png"],
        "jpeg": ["pdf", "png"],
        "png": ["pdf", "jpg"],
        "mp3": ["wav"],
        "wav": ["mp3"],
    }
    return target_ext in supported.get(source_ext, [])

def save_uploaded_file(uploaded_file, folder="temp_uploads"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path
