import boto3
from app.config import settings
from app.constants import AUDIO_UPLOAD_FOLDER
from botocore.exceptions import BotoCoreError, ClientError

polly_client = boto3.client("polly", region_name="ap-southeast-1")
s3_client = boto3.client("s3", region_name="ap-southeast-1")


def generate_voice_and_mark(text, s3_key_prefix: str = AUDIO_UPLOAD_FOLDER):
    try:
        voice_response = polly_client.synthesize_speech(
            Text=text, TextType="text", OutputFormat="mp3", VoiceId="Joanna"
        )

        audio_stream = voice_response["AudioStream"].read()
        audio_key = f"{s3_key_prefix}/raw.mp3"

        s3_client.put_object(
            Bucket=settings.AWS_BUCKET_NAME,
            Key=audio_key,
            Body=audio_stream,
            ContentType="audio/mpeg",
        )
        print(f"Audio uploaded to S3: {audio_key}")

    except (BotoCoreError, ClientError) as e:
        print("Failed to generate or save audio:", e)
        return "Error"

    try:
        mark_response = polly_client.synthesize_speech(
            Text=text,
            TextType="text",
            VoiceId="Joanna",
            OutputFormat="json",
            SpeechMarkTypes=["word"],
        )

        with open("mark.marks", "wb") as f:
            f.write(mark_response["AudioStream"].read())
        print("Speech marks saved successfully.")

    except (BotoCoreError, ClientError) as e:
        print("Failed to generate or save speech marks:", e)
        return "Error"

    return "Success"
