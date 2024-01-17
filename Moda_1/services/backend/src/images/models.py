from sqlalchemy import JSON, Boolean, Table, Column, Integer, String, TIMESTAMP, MetaData, ForeignKey
from datetime import datetime

from auth.models import user

metadata = MetaData()

image = Table(
    "image",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(user.c.id), nullable=False),
    Column("filename", String, nullable=False),
    Column("date_uploaded", TIMESTAMP, default=datetime.utcnow),
    Column("description", String),
    Column("is_approved", Boolean, default=False),
    Column("tags", JSON),
)
