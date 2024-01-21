from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class Product(BaseModel):
    id: int = Field(description="index")
    user_id: int = Field(description="유저 id")
    category: str = Field(description="카테고리")
    price: str = Field(description="가격")
    cost: str = Field(description="원가")
    name: str = Field(description="상품명")
    description: str = Field(description="상품 설명")
    barcode: str = Field(description="상품 설명")
    expration_date: datetime = Field(description="유통기한")
    size: str = Field(description="상품 크기")

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "user_id": 4,
                "category": "커피",
                "price": "4500",
                "cost": "2000",
                "name": "아메리카노",
                "description": "케냐 원두로 만든 아메리카노",
                "barcode": "3243565165",
                "expration_date": "2024-12-31",
                "size": "small"
            }
        }


