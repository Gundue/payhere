from datetime import datetime, timedelta
import hashlib
import jwt
from fastapi import Depends, HTTPException, status

import models

__secret = "payhere"


def encode_jwt(phone: str, minutes=0):
    encoded_data = hashlib.sha256(
        str(f"{phone}").encode()
    ).hexdigest()
    payload = {
        "data": encoded_data,
        "exp": datetime.utcnow() + timedelta(minutes=minutes),
    }
    return jwt.encode(payload, __secret, algorithm="HS256")


def chk_access_token(get_token: models.Token, access_token: str):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        access_token = access_token.replace("Bearer ", "")
        payload = jwt.decode(access_token, key=__secret, algorithms=["HS256"])

        return get_token.access_token == access_token

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )