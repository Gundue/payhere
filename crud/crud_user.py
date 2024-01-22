from sqlalchemy.orm import Session
from schemas import user_schema
import models


def create_user(db: Session, user: user_schema.User):
    db_user = models.User(
        phone=user.phone,
        password=user.password,
        name=user.name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"success": "User create"}


def read_user(db: Session, phone: str):
    return(
        db.query(models.User)
        .filter(
            (models.User.phone == phone)
        )
        .first()
    )