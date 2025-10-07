from jose import jwt, JWTError
from passlib.context import CryptContext
from src.garbage_collector.core.config import setting
from datetime import datetime, timedelta
from fastapi import HTTPException

SECRET = setting.SECRET
ALGORITHM = setting.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRY = setting.ACCESS_TOKEN_EXPIRTY_TIMEOUT

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)


def verify_password(plain_password, hashed_password) -> str:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(data: dict, expiry: timedelta = None) -> str:
    to_encode = data.copy()
    token_expiry = datetime.utcnow() + (
        expiry or timedelta(minutes=ACCESS_TOKEN_EXPIRY)
    )
    payload_claim = {"exp": token_expiry}
    to_encode.update(payload_claim)
    created_token = jwt.encode(claims=to_encode, key=SECRET, algorithm=ALGORITHM)
    return created_token


def decode_token(token: str):
    try:
        payload = jwt.decode(token=token, key=SECRET, algorithms=ALGORITHM)
        return payload
    except JWTError as e:
        raise HTTPException(400, f"JWT Error : {e}")
