from datetime import datetime as dt
from fastapi import Depends, FastAPI, Response
from fastapi.responses import RedirectResponse
from fastapi_users import FastAPIUsers

from auth.base_config import auth_backend, fastapi_users, current_user
from auth.schemas import UserRead, UserCreate
from fastapi.middleware.cors import CORSMiddleware

from auth.models import User, UserOut
from auth.manager import get_user_manager

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

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.get("/user", response_model=UserOut)
def protected_route(user: User = Depends(current_user)):
    user.registered_at = dt.strftime(user.registered_at, "%m/%d/%Y, %H:%M:%S")
    return user

@app.get("/")
def home():
    return "Hello, CTF Competitor!"