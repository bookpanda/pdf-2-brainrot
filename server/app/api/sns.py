import json
import urllib.parse

import requests
from app.config import settings
from app.data.s3 import upload_videos_to_s3
from app.extensions import limiter
from app.polly import generate_voice_and_mark
from app.textract import get_text_from_pdf
from app.video_generation import generate_brainrot
from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/webhook")
@limiter.limit(f"{settings.RATE_LIMIT_PER_DAY}/day")
async def sns_webhook(request: Request):
    body = await request.json()

    # handle sns subscription confirmation
    if "SubscribeURL" in body:
        subscribe_url = body["SubscribeURL"]
        print(f"Confirming SNS Subscription: {subscribe_url}")
        requests.get(subscribe_url)  # confirm the subscription
        return {"message": "SNS subscription confirmed"}

    # sns notifications
    if "Message" in body:
        sns_message = json.loads(body["Message"])
        # print(f"Received SNS Event: {sns_message}")
        if sns_message["Records"][0]["eventName"] == "ObjectCreated:Put":
            key = sns_message["Records"][0]["s3"]["object"]["key"]
            decoded_key = urllib.parse.unquote_plus(key)
            prefix, key = decoded_key.split("/")
            print(f"Key from SNS: {key}, prefix: {prefix}")
            if prefix == "pdfs":
                text = get_text_from_pdf(decoded_key)
                print(f"Text from Textract: {text}")
                if text == "Error":
                    return {"message": "Textract Error"}
                if generate_voice_and_mark(text) == "Error":
                    return {"message": "Polly Error"}
                generate_brainrot()
                upload_videos_to_s3(key)

    return {"message": "SNS notification received"}
