from sqlalchemy import update
from sqlalchemy.orm import Session
from schemas import token_schema
from datetime import datetime
import models


def create_token(db: Session, token: token_schema.Token):
    db_token = models.Token(
        user_id=token.user_id,
        access_token=token.access_token,
        created_at=token.created_at
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return {"success": "Token create"}


def read_token(db: Session, user_id: int):
    return (db.query(models.Token)
            .filter(
        (models.Token.user_id == user_id)
    )
            .all()
            )


def update_token(db: Session, token: token_schema.Token):
    db_token = (
        update(models.Token)
        .where(
            models.Token.user_id == token.user_id
        )
        .values(
            access_token=token.access_token,
            created_at=token.created_at
        )
    )
    print(db_token)
    db.execute(db_token)
    db.commit()

    return {"success": "Token updated successfully"}


def read_token_chk(db: Session, access_token: str):
    return (db.query(models.Token)
            .filter(
                (models.Token.access_token == access_token)
            )
            .first()
        )


def delete_token(db: Session, access_token:str):
    db.query(models.Token).filter(models.Token.access_token == access_token).delete()
    db.commit()

    return {"success": "Token delete"}