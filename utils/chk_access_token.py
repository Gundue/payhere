import jwt
from core.config import SECRET

import models


def chk_access_token(get_token: models.Token, access_token: str):
    if access_token is None:
        return "No token provided"
    try:
        jwt.decode(access_token, key=SECRET, algorithms=["HS256"])

        return "Token valid" if get_token.access_token == access_token else "Invalid token"
    except jwt.ExpiredSignatureError:
        return "Token has expired"
    except jwt.InvalidTokenError:
        return "Invalid token"
    except Exception as e:
        return "Token validation failed"
