import uvicorn
from fastapi import FastAPI

from core.config import setting
from db.database import engine
import models
from crud import crud_user
from routers import user,product

app = FastAPI()


models.Base.metadata.create_all(bind=engine)
app.include_router(user.router, tags=["user"])
app.include_router(product.router, tags=["product"])


if __name__ == "__main__":
    uvicorn.run(app, host=setting.host, port=setting.port)