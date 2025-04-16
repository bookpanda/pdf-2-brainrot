import requests
from app.config import settings


def get_presigned_url(filename: str) -> (str, str):
    """
    Generate a presigned URL for file upload to S3.
    """
    try:
        response = requests.post(
            f"{settings.API_URL}/pdfs/get-presigned-url/",
            json={"filename": filename},
        )

        return response.json().get("url"), response.json().get("key")

    except requests.RequestException as e:
        raise Exception(f"Failed to get presigned URL: {e}")


def get_processed_videos() -> list[dict[str, str]]:
    """
    Get all video urls from S3.
    """
    try:
        response = requests.get(f"{settings.API_URL}/videos/")
        return response.json().get("files")

    except requests.RequestException as e:
        raise Exception(f"Failed to get videos: {e}")
