from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_role
from app.core.database import get_db
from app.models.enums import UserRole
from app.models.faculty_profile import FacultyProfile
from app.models.user import User
from app.repositories import faculty_repository
from app.schemas.faculty import FacultyProfileCreate, FacultyProfileOut
from app.services import faculty_service

router = APIRouter(prefix="/faculty", tags=["faculty"])


@router.post("/me", response_model=FacultyProfileOut, status_code=status.HTTP_201_CREATED)
async def create_my_profile(
    data: FacultyProfileCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> FacultyProfile:
    return await faculty_service.create_my_profile(db, current_user, data)


@router.get("/me", response_model=FacultyProfileOut)
async def get_my_profile(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> FacultyProfile:
    profile = await faculty_repository.get_by_user_id(db, current_user.id)
    if profile is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Faculty profile not found")
    return profile


@router.get("", response_model=list[FacultyProfileOut])
async def list_faculty(
    db: Annotated[AsyncSession, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(UserRole.ADMIN))],
) -> list[FacultyProfile]:
    return await faculty_repository.list_all(db)
