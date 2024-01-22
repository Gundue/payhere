from datetime import datetime, timedelta
import hashlib
import jwt

from core.config import SECRET

def encode_jwt(phone: str, minutes=0):
    encoded_data = hashlib.sha256(
        str(f"{phone}").encode()
    ).hexdigest()
    payload = {
        "data": encoded_data,
        "exp": datetime.utcnow() + timedelta(minutes=minutes),
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


