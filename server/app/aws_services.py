import boto3
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()


# Use IAM role on EC2, so no need for explicit AWS credentials
polly_client = boto3.client("polly", region_name="us-east-1")


# Request model
class PollyRequest(BaseModel):
    text: str


@app.post("/polly")
async def generate_speech(request: PollyRequest):
    """Convert text to speech using Amazon Polly and return the MP3 file."""
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")

    response = polly_client.synthesize_speech(
        Text=request.text, OutputFormat="mp3", VoiceId="Joanna"
    )

    speech_path = "speech.mp3"
    with open(speech_path, "wb") as f:
        f.write(response["AudioStream"].read())

    return FileResponse(speech_path, media_type="audio/mpeg", filename="speech.mp3")


@app.get("/")
def root():
    return {"message": "FastAPI Polly server is running!"}
