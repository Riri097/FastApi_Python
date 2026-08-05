import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

CREDENTIALS_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Shared JWT encode helper, "type" claim tells access and refresh tokens apart.
# "jti" keeps tokens unique even if minted for the same user within the same second.
def _create_token(user_id: uuid.UUID, expires_delta: timedelta, token_type: str) -> str:
    expire = datetime.now(UTC) + expires_delta
    payload = {"sub": str(user_id), "exp": expire, "type": token_type, "jti": uuid.uuid4().hex}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_access_token(user_id: uuid.UUID) -> str:
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_token(user_id, expires_delta, "access")


def create_refresh_token(user_id: uuid.UUID) -> str:
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    return _create_token(user_id, expires_delta, "refresh")


def _decode_token(token: str, expected_type: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as exc:
        raise CREDENTIALS_ERROR from exc
    if payload.get("type") != expected_type:
        raise CREDENTIALS_ERROR
    return payload


def decode_access_token(token: str) -> dict[str, Any]:
    return _decode_token(token, "access")


def decode_refresh_token(token: str) -> dict[str, Any]:
    return _decode_token(token, "refresh")
