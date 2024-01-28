from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from fastapi.middleware.cors import CORSMiddleware

from auth.models import User
from auth.manager import get_user_manager

app = FastAPI(
    title="Moda"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return "Hello, World!"