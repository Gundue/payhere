from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class UserSocial(BaseModel):
    phone: str = Field(description="phone number")
    password: str = Field(description="user password")

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "phone": "01011111111",
                "password": "dasjhkjajhdl1!&dasda4856",
            }
        }