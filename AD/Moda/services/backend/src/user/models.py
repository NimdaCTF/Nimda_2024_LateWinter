from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, MetaData, String, Table

from auth.models import user

from database import Base

metadata = MetaData()

image = Table(
    "image",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(user.c.id), nullable=False),
    Column("file_key", String, nullable=False),
    Column("content_type", String, nullable=False),
    Column("file_size", Integer, nullable=False),
    Column("date_uploaded", TIMESTAMP, default=datetime.utcnow), 
)

class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey(user.c.id), index=True, nullable=False)
    file_key = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    date_uploaded = Column(TIMESTAMP, default=datetime.utcnow)
