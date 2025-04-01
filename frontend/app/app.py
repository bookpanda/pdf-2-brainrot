import requests
import streamlit as st

st.title("PDF to Brainrot")
st.write("Hi yall! This is a simple app that converts PDF files to brainrot.")

st.write("Upload your PDF file below:")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.write(f"File uploaded: {uploaded_file.name}")

    if st.button("Convert to Brainrot Shorts"):
        files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}

        response = requests.post(
            "https://example.com/convert_to_brainrot",
            files=files,
        )

        if response.status_code == 200:
            st.success("Successfully converted to Brainrot Shorts!")
            st.write(response.json().get("brainrot_shorts"))
        else:
            st.error(f"Conversion failed, status code: {response.status_code}")
