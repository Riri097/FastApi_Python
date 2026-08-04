import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.db.session import get_db
from app.models import RefreshToken, User
from app.schemas import LoginRequest, RefreshTokenRequest, TokenResponse, UserCreate, UserOut

router = APIRouter(tags=["auth"])


# Persists a new refresh token row for a user
async def _store_refresh_token(db: AsyncSession, user_id, token: str) -> None:
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    db.add(RefreshToken(user_id=user_id, token=token, expires_at=expires_at))


# Some DB backends (e.g. SQLite) drop tzinfo on round-trip; normalize to UTC-aware
def _is_expired(expires_at: datetime) -> bool:
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)
    return expires_at < datetime.now(timezone.utc)


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == user_in.email))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")

    user = User(email=user_in.email, hashed_password=hash_password(user_in.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Incorrect email or password")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    await _store_refresh_token(db, user.id, refresh_token)
    await db.commit()
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    payload = decode_refresh_token(body.refresh_token)

    result = await db.execute(select(RefreshToken).where(RefreshToken.token == body.refresh_token))
    stored = result.scalar_one_or_none()
    if stored is None or stored.revoked or _is_expired(stored.expires_at):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired refresh token")

    # Rotate: revoke the old refresh token and issue a new pair
    stored.revoked = True
    user_id = uuid.UUID(payload["sub"])
    new_access_token = create_access_token(user_id)
    new_refresh_token = create_refresh_token(user_id)
    await _store_refresh_token(db, user_id, new_refresh_token)
    await db.commit()
    return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(body: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == body.refresh_token))
    stored = result.scalar_one_or_none()
    if stored is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid refresh token")

    stored.revoked = True
    await db.commit()
