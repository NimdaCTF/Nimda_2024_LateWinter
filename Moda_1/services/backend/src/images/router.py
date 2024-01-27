from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from images.models import image
from images.schemas import ImageCreate

router = APIRouter(
    prefix="/images",
    tags=["Image"]
)

@router.get("/")
async def get_all_images(filename: str, session: AsyncSession = Depends(get_async_session)):
    query = select(image).where(image.c.filename == filename)
    result = await session.execute(query)
    return result.mappings().all()

@router.get("/{image_id}")
async def get_specific_images(image_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(image).where(image.c.id == image_id)
    result = await session.execute(query)
    return result.mappings().all()

@router.post("/")
async def add_specific_images(new_image: ImageCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(image).values(**new_image.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
