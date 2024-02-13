    
from datetime import datetime
from pydantic import BaseModel


class ImageCreate(BaseModel):
    user_id: int
    file_key: str
    content_type: str
    file_size: int
    date_uploaded: datetime = datetime.utcnow()