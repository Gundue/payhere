from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from crud.crud_user import read_user, create_user
from db.database import engine
import models
from schemas import user_schema
from routers import get_db

prefix = "user"
models.Base.metadata.create_all(bind=engine)
router = APIRouter(prefix=f"/{prefix}", responses={401: {"a": "a"}})

@router.post("")
async def post_user(user: user_schema.User,  db: Session = Depends(get_db)):
    """
    create user
    """
    if read_user(db, phone=user.phone) is None:
        response = create_user(db, user)
    else:
        response = {"fail": "already exist"}

    return response
