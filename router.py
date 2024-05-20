import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from database import UsersCreds, UserLog, UserReg

router = APIRouter(
    prefix="/user",
    tags=['Пользователи']
)

router_cred = APIRouter(
    tags=["Регистрация/Логин"]
)


@router_cred.get("/")
async def root():
    return {"message": "Hello World"}


@router_cred.post("/registration")
async def registration(user_reg: Annotated[UserReg, Depends()]) -> str:
    user_reg_ok = UsersCreds.user_registration(user_reg)
    return user_reg_ok


@router.post("/search")
async def search():
    return {"message": "Hello World"}


@router.get("/{user_id}")
async def user():
    return {"message": "Hello World"}


@router_cred.post("/login")
def say_hello(user_log: Annotated[UserLog, Depends()]) -> str:
    user_log_ok = UsersCreds.user_login(user_log)
    return user_log_ok
