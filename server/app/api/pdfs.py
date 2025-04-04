from app.api.dtos.pdf import GetPresignedUrl
from app.constants import PDF_MIME_TYPE, PDF_UPLOAD_FOLDER
from app.data.s3 import generate_presigned_url
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.post("/get-presigned-url/")
def get_presigned_url(presigned_url_request: GetPresignedUrl) -> dict[str, str]:
    """
    Generate a presigned URL for file upload to S3.
    """
    try:
        presigned_url = generate_presigned_url(
            PDF_UPLOAD_FOLDER, presigned_url_request.filename, PDF_MIME_TYPE
        )

        return {"url": presigned_url}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
