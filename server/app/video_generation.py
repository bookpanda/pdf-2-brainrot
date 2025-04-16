import json

import cv2
import numpy as np
from app.utils import get_random_file_path
from moviepy.editor import AudioFileClip, VideoFileClip


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
    target_width, target_height = int(frame_width * 0.5), int(frame_height * 0.5)

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(
        "./generated/output_video_with_text.mkv",
        fourcc,
        fps,
        (target_width, target_height),
    )

    frame_index = 0
    word_index = 0
    text = ""
    current_time = 0
    # skip_rate = 2  # Skip every 2 frames
    while cap.isOpened():
        if max_time < current_time:
            break
        # if frame_index % skip_rate != 0:
        #     frame_index += 1
        #     cap.read()
        #     continue

        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (target_width, target_height))
        # Calculate the current time in seconds
        current_time = frame_index / fps

        # Add text to the frame if it's time to show the next word
        if word_index < len(words_data):
            if words_data[word_index]["time"] / 1000.0 <= current_time:
                text = words_data[word_index]["value"]
                word_index += 1

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        font_color = (255, 255, 255)  # White
        thickness = 4
        outline_thickness = 6

        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        text_width, text_height = text_size

        x = (target_width - text_width) // 2
        y = (target_height + text_height) // 2

        # Add the outline by drawing the text multiple times with different positions and a larger thickness
        # Outline effect (draw in all directions)
        cv2.putText(
            frame,
            text,
            (x - 3, y - 3),
            font,
            font_scale,
            (0, 0, 0),
            outline_thickness,
            cv2.LINE_AA,
        )  # Top-left
        cv2.putText(
            frame,
            text,
            (x + 3, y - 3),
            font,
            font_scale,
            (0, 0, 0),
            outline_thickness,
            cv2.LINE_AA,
        )  # Top-right
        cv2.putText(
            frame,
            text,
            (x - 3, y + 3),
            font,
            font_scale,
            (0, 0, 0),
            outline_thickness,
            cv2.LINE_AA,
        )  # Bottom-left
        cv2.putText(
            frame,
            text,
            (x + 3, y + 3),
            font,
            font_scale,
            (0, 0, 0),
            outline_thickness,
            cv2.LINE_AA,
        )  # Bottom-right
        # Add the word to the frame (at the calculated position)
        cv2.putText(
            frame, text, (x, y), font, font_scale, font_color, thickness, cv2.LINE_AA
        )

        # Write the processed frame to the output video
        out.write(frame)
        frame_index += 1

    # Release the video capture and writer objects
    cap.release()
    out.release()

    return 1


def add_voice_to_video(video_path, voice_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(voice_path)

    if audio_clip.duration > video_clip.duration:
        # Trim the audio to the video's duration (if audio is longer than the video)
        audio_clip = audio_clip.subclip(0, video_clip.duration)
    else:
        # Trim the video to the audio's duration (if video is longer than the audio)
        video_clip = video_clip.subclip(0, audio_clip.duration)

    video_clip = video_clip.set_audio(audio_clip)
    video_clip.write_videofile("./generated/brainrotted.mp4", codec="libx264")
    return 0


def generate_brainrot():
    video_path = get_random_file_path("./videos")
    voice_path = "./generated/raw.mp3"
    marks_path = "./generated/mark.marks"

    add_text_to_video(video_path, marks_path, voice_path)
    add_voice_to_video("./generated/output_video_with_text.mkv", voice_path)


# mp4 -> mp4: 1.50
