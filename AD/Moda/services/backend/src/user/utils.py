from user.schemas import ImageCreate
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from user.models import image


async def create_image_record(new_image: ImageCreate, session: AsyncSession):
    stmt = insert(image).values(**new_image.model_dump())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}