from pydantic_settings import BaseSettings

HOST = "127.0.0.1"
PORT = 8000

SECRET = "payhere"


class Settings(BaseSettings):
    host: str
    port: int


setting = Settings(host=HOST, port=PORT)