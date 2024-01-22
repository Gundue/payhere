from datetime import datetime
from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int = Field(description="Idx")
    user_id: int = Field(description="User Idx")
    category: str = Field(description="Product category")
    price: str = Field(description="Product price")
    cost: str = Field(description="Product cost")
    name: str = Field(description="Product name")
    description: str = Field(description="Product description")
    barcode: str = Field(description="Product barcode")
    expiration_date: datetime = Field(description="Product Expiration date")
    size: str = Field(description="Product size")

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "category": "음료",
                "price": "6000",
                "cost": "2000",
                "name": "슈크림 라떼",
                "description": "슈크림을 올린 라떼",
                "barcode": "01001010110",
                "expiration_date": datetime.now(),
                "size": "small"
            }
        }


class CreateProduct(BaseModel):
    user_id: int = Field(description="User Idx")
    category: str = Field(description="Product category")
    price: str = Field(description="Product price")
    cost: str = Field(description="Product cost")
    name: str = Field(description="Product name")
    description: str = Field(description="Product description")
    barcode: str = Field(description="Product barcode")
    expiration_date: datetime = Field(description="Product Expiration date")
    size: str = Field(description="Product size")

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "user_id": 1,
                "category": "음료",
                "price": "6000",
                "cost": "2000",
                "name": "슈크림 라떼",
                "description": "슈크림을 올린 라떼",
                "barcode": "01001010110",
                "expiration_date": datetime.now(),
                "size": "small"
            }
        }


