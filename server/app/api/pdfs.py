from typing import Dict

from app.data.s3 import generate_presigned_url
from app.models.pdf import FileRequest
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/")
def get_items():
    return {"message": "List of items"}


# @router.post("/")
# def create_item(item: Item):
#     return {"message": f"Item {item.name} created!"}


@router.post("/get-presigned-url/")
def get_presigned_url(file_request: FileRequest) -> Dict[str, str]:
    """
    Generate a presigned URL for file upload to S3.
    """
    try:
        presigned_url = generate_presigned_url(
            file_request.filename, file_request.file_type
        )

        return {"url": presigned_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
