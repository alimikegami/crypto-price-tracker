from jose import jwt
from datetime import timedelta, datetime, timezone

def createAccessToken(data: dict, expiredIn: int, secretKey: str, algorithm: str) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expiredIn)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, secretKey, algorithm)

    return encoded_jwt