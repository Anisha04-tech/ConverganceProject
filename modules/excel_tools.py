import pandas as pd
import streamlit as st
import tempfile

def excel_to_csv(uploaded_file):
    try:
        df = pd.read_excel(uploaded_file)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            df.to_csv(tmp.name, index=False)
            st.success("Excel converted to CSV successfully.")
            with open(tmp.name, "rb") as f:
                st.download_button("Download CSV", f, file_name="converted.csv")
    except Exception as e:
        st.error(f"Excel conversion failed: {e}")