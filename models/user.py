from sqlalchemy import Column, Integer, String

from db.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    phone = Column(String(11))
    password = Column(String(128))
    name = Column(String(10))
