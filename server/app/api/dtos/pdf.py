from pydantic import BaseModel


class GetPresignedUrl(BaseModel):
    filename: str
