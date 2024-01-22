from pydantic import BaseModel, Field


class User(BaseModel):
    phone: str = Field(description="Phone Number")
    password: str = Field(description="User password")
    name: str = Field(description="User name")

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "phone": "01011111111",
                "password": "1234",
                "name": "park"
            }
        }


class UserLogin(BaseModel):
    phone: str = Field(description="Phone Number")
    password: str = Field(description="User password")

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "phone": "01011111111",
                "password": "1234",
            }
        }
