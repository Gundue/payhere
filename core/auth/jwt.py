from datetime import datetime, timedelta
import hashlib
import jwt


__secret = "payhere"


def encode_jwt(phone: str, days=0, minutes=0):
    encoded_data = hashlib.sha256(
        str(f"{phone}").encode()
    ).hexdigest()
    payload = {
        "data": encoded_data,
        "exp": datetime.utcnow() + timedelta(days=days, minutes=minutes),
    }
    return jwt.encode(payload, __secret, algorithm="HS256")