import uuid

import boto3
from app.config import settings
from botocore.exceptions import ClientError, NoCredentialsError

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
    endpoint_url=f"https://s3-{settings.AWS_REGION}.amazonaws.com",
)


def generate_presigned_url(folder: str, filename: str, file_type: str):
    """
    Generate a presigned URL to allow clients to upload a file to S3.

    :param filename: Name of the file to be uploaded
    :param file_type: MIME type of the file (e.g., 'image/jpeg')
    :return: Presigned URL
    """
    try:
        name, ext = filename.rsplit(".", 1)
        random_suffix = uuid.uuid4().hex[:8]
        unique_filename = f"{name}_{random_suffix}.{ext}"
        s3_key = f"{folder}/{unique_filename}"

        response = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.AWS_BUCKET_NAME,
                "Key": s3_key,
                "ContentType": file_type,
            },
            ExpiresIn=3600,
        )

        return response
    except (NoCredentialsError, ClientError) as e:
        raise Exception(f"Error generating presigned URL: {e}")
