from datetime import datetime
from uuid import uuid4

from fastapi import Depends, HTTPException, UploadFile, status, APIRouter
from fastapi_users import schemas
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from user.models import image
from user.utils import create_image_record
from user.schemas import ImageCreate
from auth.models import User
from auth.manager import UserManager, get_user_manager
from auth.schemas import UserOut, UserUpdate
from auth.base_config import current_user

from config import settings

from database import get_async_session
from s3 import generate_presigned_url, s3_upload

router = APIRouter(
    tags=["user"],
    prefix="/user"
)

@router.get("/", response_model=UserOut)
def get_current_user(user: User = Depends(current_user)):
    user.registered_at = datetime.strftime(user.registered_at, "%m/%d/%Y, %H:%M:%S")
    return user

@router.put("/update", response_model=UserUpdate)
async def update_user(
    user_update: UserUpdate,
    current_user: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    updated_user = await user_manager.update(user_update, current_user)
    return updated_user

@router.get("/image")
async def get_latest_user_image(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    query = select(image.c.file_key).where(image.c.user_id == user.id).order_by(desc(image.c.date_uploaded)).limit(1)
    result = await session.execute(query)
    first_result = result.mappings().first()

    if first_result is None or not hasattr(first_result, 'file_key'):
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="User has no images"
        )
    
    image_key = first_result.file_key
    presigned_url = generate_presigned_url(image_key)
    return presigned_url

@router.post("/image")
async def upload(file: UploadFile = None, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No file to upload'
        )
        
    content = await file.read()
    file_size = len(content)
    
    if not 0 < file_size <= 1024*1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Uploaded file is too big. Supported size is 0 - 1 MB'
        )
        
    content_type = file.content_type
        
    if content_type not in settings.SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Unsupported file type. Supported types are JPEG, PNG, and PDF'
        )
        
    image_id = uuid4()
    await create_image_record(
        new_image=ImageCreate(
            user_id=user.id,
            file_key=f'{image_id}.{settings.SUPPORTED_FILE_TYPES[content_type]}',
            content_type=content_type,
            file_size=file_size,
            date_uploaded=datetime.utcnow()
        ),
        session = session
    )
    
    s3_upload(content=content, key=f'{image_id}.{settings.SUPPORTED_FILE_TYPES[content_type]}')
    return {"status": "success"}
        
#https://www.youtube.com/watch?v=727l8Asu8P0?t=5:00
#Уязвимость можно создать, если узнавать расширение файла из его названия