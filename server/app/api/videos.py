from app.data.s3 import get_files_in_folder, get_url_by_key
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
def get_all_videos():
    """
    Get all video urls in the S3 bucket.
    """
    try:
        files = get_files_in_folder("videos")

        return {"files": files}
    except HTTPException as e:
        raise e


@router.get("/{key_name}")
def get_video_by_key(key_name: str):
    """
    Get a video by its key from the S3 bucket.
    """
    try:
        url = get_url_by_key(f"videos/{key_name}")

        return {"url": url}
    except HTTPException as e:
        raise e
