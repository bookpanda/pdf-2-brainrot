from app.data.s3 import get_files_in_folder
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
def get_all_videos():
    """
    Get all video urls in the S3 bucket.
    """
    try:
        files = get_files_in_folder("videos")
        print(files)

        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.get("/{key_name}")
# def get_video_by_key(key_name: str):
#     """
#     Get a file by its key from the S3 bucket.
#     """
#     try:
#         file = get_file_by_key(f"videos/{key_name}")

#         return {"file": file}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
