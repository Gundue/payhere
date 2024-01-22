import bcrypt
from datetime import datetime

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

import models
from crud.crud_user import read_user, create_user
from crud.crud_token import (
    create_token, read_token, update_token, find_token_exists, delete_token
)
from core.auth.jwt_manage import encode_jwt
from db.database import engine
from schemas import user_schema, token_schema
from routers import get_db
from utils.response import custom_response
from utils.validate_phone_number import validate_phone_number


prefix = "user"
models.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix=f"/{prefix}")


@router.post("/create")
async def user_create(user: user_schema.User,  db: Session = Depends(get_db)):
    """
    `회원 가입`
    """
    get_user = read_user(db, phone=user.phone)
    if get_user is None and validate_phone_number(user.phone):
        hash_pw = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
        user.password = hash_pw
        create_user(db, user)
        return custom_response(code=200, message="Success Create")
    else:
        return custom_response(code=400, message="Invalid User")


@router.post("/login")
async def user_login(user: user_schema.UserLogin,  db: Session = Depends(get_db)):
    """
    `로그인`
    """
    get_user = read_user(db, phone=user.phone)
    if get_user is None:
        return custom_response(code=401, message="User does not exist")

    if not bcrypt.checkpw(user.password.encode("utf-8"), get_user.password.encode("utf-8")):
        return custom_response(code=401, message="Password mismatch")

    access_token = encode_jwt(user.phone, minutes=60)
    token = token_schema.Token(user_id=get_user.id, access_token=access_token, create_at=datetime.now())
    # 기존 토큰이 존재한다면 DB에 저장된 토큰과 같은지 검사 후 새로운 토큰 발급
    if read_token(db, get_user.id):
        update_token(db, token)
    else:
        create_token(db, token)
    return custom_response(code=200, message=access_token)


@router.get("/logout")
async def user_logout(
        db: Session = Depends(get_db),
        access_token: str = Header(None, convert_underscores=False)
):
    """
    `로그아웃`
    """
    get_token = find_token_exists(db, access_token)
    if get_token:
        delete_token(db, access_token)
        return custom_response(code=200, message="Success Logout")
    else:
        return custom_response(code=401, message="No token provided")



