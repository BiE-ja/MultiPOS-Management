from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt
from typing import Any
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode = {"exp": expire, "sub": str(data)}  # type: ignore
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)  # type: ignore
    return encoded_jwt


def decode_access_token(token: str):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    return payload
