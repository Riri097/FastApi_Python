import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_role
from app.core.database import get_db
from app.models.enums import UserRole
from app.models.student_profile import StudentProfile
from app.models.user import User
from app.repositories import student_repository
from app.schemas.student import StudentProfileCreate, StudentProfileOut
from app.services import student_service

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/me", response_model=StudentProfileOut, status_code=status.HTTP_201_CREATED)
async def create_my_profile(
    data: StudentProfileCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> StudentProfile:
    return await student_service.create_my_profile(db, current_user, data)


@router.get("/me", response_model=StudentProfileOut)
async def get_my_profile(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> StudentProfile:
    profile = await student_repository.get_by_user_id(db, current_user.id)
    if profile is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Student profile not found")
    return profile


@router.get("", response_model=list[StudentProfileOut])
async def list_students(
    db: Annotated[AsyncSession, Depends(get_db)],
    _reviewer: Annotated[User, Depends(require_role(UserRole.ADMIN, UserRole.TEACHER))],
) -> list[StudentProfile]:
    return await student_repository.list_all(db)


@router.get("/{student_id}", response_model=StudentProfileOut)
async def get_student(
    student_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _reviewer: Annotated[User, Depends(require_role(UserRole.ADMIN, UserRole.TEACHER))],
) -> StudentProfile:
    profile = await student_repository.get_by_id(db, student_id)
    if profile is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Student not found")
    return profile
