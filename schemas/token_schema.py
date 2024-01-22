from datetime import datetime
from pydantic import BaseModel, Field


class Token(BaseModel):
    user_id: int = Field(description="phone number")
    access_token: str = Field(description="user password")
    created_at: datetime = datetime.now()

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "user_id": "1",
                "access_token": "dasjhkjajhdl1!&dasda4856",
                "created_at": "tom"
            }
        }