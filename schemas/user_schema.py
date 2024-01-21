from datetime import datetime
from pydantic import BaseModel, Field


class User(BaseModel):
    phone: str = Field(description="phone number")
    password: str = Field(description="user password")
    name: str = Field(description="user name")

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "phone": "01011111111",
                "password": "dasjhkjajhdl1!&dasda4856",
                "name": "tom"
            }
        }


class UserLogin(BaseModel):
    phone: str = Field(description="phone number")
    password: str = Field(description="login password")

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "phone": "01011111111",
                "password": "dasjhkjajhdl1!&dasda4856",
            }
        }
