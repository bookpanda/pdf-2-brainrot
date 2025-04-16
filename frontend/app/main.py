import sys
from pathlib import Path

import requests
import streamlit as st

# Add the project root to the Python path (for streamlit to find the app module)
sys.path.append(str(Path(__file__).parent.parent))
from app.utils import get_presigned_url, get_processed_videos

st.title("PDF to Brainrot")
st.write("Hi yall! This is a simple app that converts PDF files to brainrot.")

st.write("Upload your PDF file below:")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if "uploaded_key" not in st.session_state:
    st.session_state.uploaded_key = None

if uploaded_file is not None:
    st.write(f"File uploaded: {uploaded_file.name}")

    if st.session_state.uploaded_key != uploaded_file.name:
        if st.button("Convert to Brainrot Shorts"):
            presigned_url, key = get_presigned_url(uploaded_file.name)
            file_bytes = uploaded_file.getvalue()

            response = requests.put(
                presigned_url,
                data=file_bytes,
                headers={"Content-Type": "application/pdf"},
            )

            if response.status_code == 200:
                st.session_state.uploaded_key = uploaded_file.name  # mark as processed
                st.success("Converting to Brainrot Shorts! Please wait...")
                st.write(f"Key: {key}")
            else:
                st.error(f"Conversion failed, status code: {response.status_code}")
    else:
        st.warning("This file has already been processed. Please upload a new one.")


# ---- Display Processed Videos ----
st.subheader("Processed Brainrot Shorts")
video_files = get_processed_videos()

if video_files:
    print(f"video_files: {len(video_files)}")
    num_columns = 3
    columns = st.columns(num_columns)

    for i in range(0, len(video_files), num_columns):
        cols = st.columns(num_columns)
        for j, video in enumerate(video_files[i : i + num_columns]):
            with cols[j]:
                st.video(video["url"])
                st.write(f"**{video['key']}**")
else:
    st.write("No processed videos available.")
