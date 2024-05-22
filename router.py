import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Body

from database import UsersCreds, UserLog, UserReg, UserSearch, UserSearchId

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
async def registration(user_reg: Annotated[UserReg, Depends(), Body()]) -> str:
    user_reg_ok = UsersCreds.user_registration(user_reg)
    return user_reg_ok


@router.post("/search")
async def search(user_search: Annotated[UserSearch, Depends()]):
    user_search = UsersCreds.search_user(user_search)
    return user_search


@router.get("/{user_id}")
async def user_by_id(user_id: Annotated[UserSearchId, Depends()]) -> UserReg:
    user_search_id = UsersCreds.get_user_by_id(user_id)
    return user_search_id


@router_cred.post("/login")
def login(user_log: Annotated[UserLog, Depends(), Body()]) -> str:
    user_log_ok = UsersCreds.user_login(user_log)
    return user_log_ok
