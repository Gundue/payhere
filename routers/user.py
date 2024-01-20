import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from crud.crud_user import read_user, create_user
from core.auth.jwt import encode_jwt
from db.database import engine
import models
from schemas import user_schema
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
async def lgoin(user: user_schema.UserLogin,  db: Session = Depends(get_db)):
    """
    `로그인`
    """
    get_user = read_user(db, phone=user.phone)
    if get_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist")

    stored_password_bytes = get_user.password.encode("utf-8")
    input_password_bytes = user.password.encode("utf-8")

    # 비밀번호 검증
    if bcrypt.checkpw(input_password_bytes, stored_password_bytes):
        return encode_jwt(user.phone, days=7)
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


