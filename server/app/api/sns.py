import json
import urllib.parse
import requests
from fastapi import APIRouter, Request

from app.textract import get_text_from_pdf

router = APIRouter()


@router.post("/webhook")
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
            prefix = key.split("/")[0]
            if(prefix == 'pdfs'):
                decoded_key = urllib.parse.unquote_plus(key)
                text = get_text_from_pdf(decoded_key)
                if(text == "Error"):return {"message": "Failed to extract text from PDF"}


    return {"message": "SNS notification received"}
