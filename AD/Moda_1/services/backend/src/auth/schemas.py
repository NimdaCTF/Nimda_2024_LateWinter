from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel

class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    
class UserUpdate(schemas.BaseUserUpdate):
    pass

class UserOut(BaseModel):
    id: int
    email: str
    username: str
    registered_at: str
    
class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None