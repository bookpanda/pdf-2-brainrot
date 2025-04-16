import sys
import time
from pathlib import Path

import requests
import streamlit as st

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))
from app.utils import get_presigned_url, get_processed_videos

st.title("PDF to Brainrot")
st.write("Hi yall! This is a simple app that converts PDF files to brainrot.")

# Initialize session state flags
if "uploaded_key" not in st.session_state:
    st.session_state.uploaded_key = None
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

uploaded_file = st.file_uploader(
    "Choose a PDF file", type="pdf", disabled=st.session_state.is_processing
)

if uploaded_file is not None:
    st.write(f"File uploaded: {uploaded_file.name}")
    convert_disabled = (
        st.session_state.is_processing
        or st.session_state.uploaded_key == uploaded_file.name
    )

    if st.button("Convert to Brainrot Shorts", disabled=convert_disabled):
        presigned_url, key = get_presigned_url(uploaded_file.name)
        file_bytes = uploaded_file.getvalue()

        response = requests.put(
            presigned_url,
            data=file_bytes,
            headers={"Content-Type": "application/pdf"},
        )

        if response.status_code == 200:
            st.session_state.is_processing = True
            st.session_state.uploaded_key = uploaded_file.name
            st.success("Upload successful. Now converting to Brainrot Shorts!")

            # Polling for processed video
            with st.spinner("Waiting for processing to finish..."):
                found = False
                max_wait = 90  # seconds
                interval = 3  # seconds between polls
                start_time = time.time()
                expected_key = key.replace("pdfs/", "").replace(".pdf", ".mp4")

                while time.time() - start_time < max_wait:
                    videos = get_processed_videos()
                    if any(v["key"] == expected_key for v in videos):
                        found = True
                        break
                    time.sleep(interval)

                if found:
                    st.success(
                        "Processing complete! 🎉 Scroll down to see your Brainrot Short."
                    )
                else:
                    st.warning("Still processing. Try refreshing in a bit.")
        else:
            st.error(f"Upload failed. Status code: {response.status_code}")


# ---- Display Processed Videos ----
st.subheader("Processed Brainrot Shorts")
video_files = get_processed_videos()

if video_files:
    num_columns = 3
    for i in range(0, len(video_files), num_columns):
        cols = st.columns(num_columns)
        for j, video in enumerate(video_files[i : i + num_columns]):
            with cols[j]:
                st.video(video["url"])
                st.write(f"**{video['key']}**")
else:
    st.write("No processed videos available.")
