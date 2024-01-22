from datetime import datetime
from pydantic import BaseModel, Field


class Token(BaseModel):
    user_id: int = Field(description="User Idx")
    access_token: str = Field(description="JWT Token")
    created_at: datetime = Field(description="Token generate time")

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "user_id": "1",
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                "created_at": "2024-01-22 10:00:00"
            }
        }