import json

import requests
from fastapi import APIRouter, Request

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
        print(f"Received SNS Event: {sns_message}")

    return {"message": "SNS notification received"}
