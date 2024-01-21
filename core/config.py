from pydantic_settings import BaseSettings

HOST = "127.0.0.1"
PORT = 8888


class Settings(BaseSettings):
    host: str
    port: int


setting = Settings(host=HOST, port=PORT)