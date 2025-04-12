import boto3
from app.config import settings

polly_client = boto3.client("polly", region_name="ap-southeast-1")
s3_client = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    endpoint_url=f"https://s3-{settings.AWS_REGION}.amazonaws.com",
)

def generate_voice_and_mark(text):
    voice_response = polly_client.synthesize_speech(
        Text=text,
        TextType='text',
        OutputFormat='mp3',
        VoiceId='Joanna', 
    )
    mark_response = polly_client.synthesize_speech(
        Text=text,
        TextType='text',
        VoiceId='Joanna', 
        OutputFormat='json',
        SpeechMarkTypes=["word"]
    )

    # Save the audio stream to a file
    audio_stream = voice_response['AudioStream']
    with open("output.mp3", "wb") as f:
        f.write(audio_stream.read())
    audio_stream = mark_response['AudioStream']
    with open("mark.marks", "wb") as f:
        f.write(audio_stream.read())
