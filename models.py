from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import ENUM

from db.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    phone = Column(String(11))
    password = Column(String(128))
    name = Column(String(10))


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    category = Column(String(50))
    price = Column(String(10))
    cost = Column(String(10))
    name = Column(String(50))
    description = Column(String(100))
    barcode = Column(String(20))
    expration_date = Column(DateTime)
    size = Column(ENUM('small', 'large'))


