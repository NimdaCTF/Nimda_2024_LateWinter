from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi.middleware.cors import CORSMiddleware

from user.router import router as router_image

from auth.models import User
from auth.schemas import UserRead, UserCreate
from auth.manager import get_user_manager
from auth.base_config import auth_backend, fastapi_users

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
]

app = FastAPI(
    title="Moda"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

app.include_router(router_image)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.get("/")
def home():
    return "Hello, CTF Competitor!"