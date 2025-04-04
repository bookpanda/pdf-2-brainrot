from typing import Dict

import requests
from app.config import settings


def get_presigned_url(filename: str) -> str:
    """
    Generate a presigned URL for file upload to S3.
    """
    try:
        response = requests.post(
            f"{settings.API_URL}/get-presigned-url/",
            json={"filename": filename},
        )
        return response.json().get("url")

    except requests.RequestException as e:
        raise Exception(f"Failed to get presigned URL: {e}")
