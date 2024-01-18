import uvicorn
from fastapi import FastAPI

from core.config import setting

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host=setting.host, port=setting.port)