import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from starlette import status
from datetime import datetime

import models
from crud.crud_user import read_user, create_user
from crud.crud_token import create_token, read_token, update_token, read_token_chk, delete_token
from core.auth.jwt import encode_jwt
from db.database import engine
from schemas import user_schema, token_schema
from routers import get_db

prefix = "user"
models.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix=f"/{prefix}", responses={401: {"a": "a"}})


@router.post("/create")
async def user_create(user: user_schema.User,  db: Session = Depends(get_db)):
    """
    `회원 가입`
    """
    if read_user(db, phone=user.phone) is None:
        hash_pw = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
        user.password = hash_pw
        response = create_user(db, user)
    else:
        response = {"fail": "already exist"}
    return response


@router.post("/login")
async def login(user: user_schema.UserLogin,  db: Session = Depends(get_db)):
    """
    `로그인`
    """
    get_user = read_user(db, phone=user.phone)
    if get_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist")

    # 비밀번호 검증
    if bcrypt.checkpw(user.password.encode("utf-8"), get_user.password.encode("utf-8")):
        access_token = encode_jwt(user.phone, minutes=60)
        token = token_schema.Token(user_id=get_user.id, access_token=access_token, create_at=datetime.now())
        if read_token(db, get_user.id):
            update_token(db, token)
        else:
            create_token(db, token)
        return access_token
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


@router.get("/logout")
async def logout(
        db: Session = Depends(get_db),
        access_token: str = Header(None, convert_underscores=False)
):
    get_token = read_token_chk(db, access_token)
    if get_token:
        return delete_token(db, access_token)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")



