from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse


def custom_response(code: int, message: str, data: Optional[List] = None) -> JSONResponse:
    response_data = {"meta": {"code": code, "message": message}, "data": data}
    return JSONResponse(jsonable_encoder(response_data))