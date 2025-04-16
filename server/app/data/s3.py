import uuid

import boto3
from app.config import settings
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import HTTPException

s3_client = boto3.client(
    "s3",
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

        return {"url": response, "key": s3_key.split("/")[-1]}
    except (NoCredentialsError, ClientError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating presigned URL: {e}",
        )


def get_files_in_folder(folder: str) -> list[dict]:
    """
    List the 6 latest files in a specific S3 folder.

    :param folder: The folder path in the S3 bucket
    :return: List of file metadata (key and presigned URL)
    """
    try:
        response = s3_client.list_objects_v2(
            Bucket=settings.AWS_BUCKET_NAME,
            Prefix=folder + "/",
        )

        if "Contents" in response:
            files = [
                item
                for item in response["Contents"]
                if item["Key"] != folder + "/"  # ignore folder itself
            ]

            # Sort by LastModified (newest first) and take the latest 6
            files.sort(key=lambda x: x["LastModified"], reverse=True)
            latest_files = files[:6]

            return [
                {
                    "key": item["Key"],
                    "url": s3_client.generate_presigned_url(
                        "get_object",
                        Params={"Bucket": settings.AWS_BUCKET_NAME, "Key": item["Key"]},
                        ExpiresIn=3600,
                    ),
                }
                for item in latest_files
            ]
        else:
            return []
    except ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing files in folder '{folder}': {e}",
        )


def get_url_by_key(key: str) -> str:
    """
    Generate a presigned URL to access a file in S3.

    :param key: The S3 key of the file
    :return: Presigned URL
    :raises Exception: If the file does not exist or an error occurs
    """
    try:
        # check if the file exists in S3
        s3_client.head_object(Bucket=settings.AWS_BUCKET_NAME, Key=key)

        return s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.AWS_BUCKET_NAME, "Key": key},
            ExpiresIn=3600,
        )

    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            raise HTTPException(
                status_code=404,
                detail=f"File '{key}' not found in S3.",
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating presigned URL: {e}",
            )


def upload_file_to_s3(filepath: str, folder: str, key: str):
    s3_key = f"{folder}/{key}"

    try:
        s3_client.upload_file(filepath, settings.AWS_BUCKET_NAME, s3_key)
        print(f"Successfully uploaded {key}")
    except Exception as e:
        print(f"Error uploading {key}")


def download_file_from_s3(folder: str, key: str):
    try:
        print(f"Key: {folder}/{key}")
        s3_client.download_file(settings.AWS_BUCKET_NAME, f"{folder}/{key}", f"{key}")
        print(f"Downloaded: {f"{key}"}")
        return f"{key}"
    except Exception as e:
        print(f"Error downloading {key}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error downloading file '{key}': {e}",
        )
