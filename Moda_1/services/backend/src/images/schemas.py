from datetime import datetime

from pydantic import BaseModel


class ImageCreate(BaseModel):
    user_id: int
    filename: str
    date_uploaded: datetime = datetime.utcnow()
    description: str = ""
    is_approved: bool = False
    tags: list = []