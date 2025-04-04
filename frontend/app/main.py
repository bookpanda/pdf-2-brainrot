import requests
import streamlit as st
from app.utils import get_presigned_url

st.title("PDF to Brainrot")
st.write("Hi yall! This is a simple app that converts PDF files to brainrot.")

st.write("Upload your PDF file below:")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    st.write(f"File uploaded: {uploaded_file.name}")

    if st.button("Convert to Brainrot Shorts"):
        presigned_url, key = get_presigned_url(uploaded_file.name)
        print(f"Presigned URL: {presigned_url}, Key: {key}")
        file_bytes = uploaded_file.getvalue()

        response = requests.put(
            presigned_url,
            data=file_bytes,
            headers={"Content-Type": "application/pdf"},
        )

        print(f"response: {response.content}")

        if response.status_code == 200:
            st.success("Successfully converted to Brainrot Shorts!")
            st.write(f"Key: {key}")
            # st.write(response.json().get("brainrot_shorts"))
        else:
            st.error(f"Conversion failed, status code: {response.status_code}")
