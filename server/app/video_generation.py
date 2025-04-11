import numpy as np
import cv2
import os
import json
from moviepy.editor import VideoFileClip, AudioFileClip

def add_text_to_video(video_path, marks_path, voice_path):
    words_data = []
    audio_clip = AudioFileClip(voice_path)
    max_time = audio_clip.duration
    with open(marks_path, "r") as f:
        for line in f:
            # Strip any leading/trailing whitespace and load the JSON object from the line
            word_data = json.loads(line.strip())
            words_data.append(word_data)
    cap = cv2.VideoCapture(video_path)

    # Get video information
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter("output_video_with_text.mp4", fourcc, fps, (frame_width, frame_height))

    # Step 3: Process the video frame by frame
    frame_index = 0
    word_index = 0
    text = ""
    current_time = 0
    while cap.isOpened():
        if(max_time < current_time):
            break
        ret, frame = cap.read()
        if not ret:
            break
        
        # Calculate the current time in seconds
        current_time = frame_index / fps
        
        # Add text to the frame if it's time to show the next word
        if word_index < len(words_data):
            if words_data[word_index]["time"] / 1000.0 <= current_time:
                text = words_data[word_index]["value"]
                word_index += 1

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (255, 255, 255)  # White
        thickness = 2

        # Get the text size (width, height)
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_width, text_height = text_size

        # Calculate the position to center the text
        x = int((frame_width - text_width) / 2)  # Horizontal center
        y = int((frame_height + text_height) / 2)  # Vertical center

        # Add the word to the frame (at the calculated position)
        cv2.putText(frame, text, (x, y), font, font_scale, font_color, thickness, cv2.LINE_AA)
                

        # Write the processed frame to the output video
        out.write(frame)
        frame_index += 1

    # Release the video capture and writer objects
    cap.release()
    out.release()

    return 1

def add_voice_to_video(video_path, voice_path):
    # Load the video file
    video_clip = VideoFileClip(video_path)

    # Load the audio (your voice recording)
    audio_clip = AudioFileClip(voice_path)

    if(audio_clip.duration>video_clip.duration):
        # Trim the audio to the video's duration (if audio is longer than the video)
        audio_clip = audio_clip.subclip(0, video_clip.duration)
    else:
        # Trim the video to the audio's duration (if video is longer than the audio)
        video_clip = video_clip.subclip(0, audio_clip.duration)

    # Set the trimmed audio to the video
    video_clip = video_clip.set_audio(audio_clip)


    # Save the new video with your voice added
    video_clip.write_videofile("final_result.mp4", codec="libx264")
    return 0
def process_video(video_path, marks_path, voice_path):
    add_text_to_video(video_path, marks_path, voice_path)
    add_voice_to_video("output_video_with_text.mp4", voice_path)

if __name__ == "__main__":
    video_path = 'minecraft1.mp4'
    voice_path = 'test.mp3'
    marks_path = 'test.marks'

    process_video(video_path, marks_path, voice_path)