import speech_recognition as sr
import streamlit as st
import tempfile

def audio_to_text(uploaded_file):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    try:
        with sr.AudioFile(tmp_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            st.success("Audio converted to text successfully.")
            st.text_area("Transcript", text)
    except Exception as e:
        st.error(f"Audio conversion failed: {e}")