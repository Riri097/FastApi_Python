from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_role
from app.core.database import get_db
from app.models.enums import UserRole
from app.models.subject import Subject
from app.models.user import User
from app.repositories import subject_repository
from app.schemas.subject import SubjectCreate, SubjectOut
from app.services import subject_service

router = APIRouter(prefix="/subjects", tags=["subjects"])


@router.post("", response_model=SubjectOut, status_code=status.HTTP_201_CREATED)
async def create_subject(
    data: SubjectCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(UserRole.ADMIN))],
) -> Subject:
    return await subject_service.create_subject(db, data)


@router.get("", response_model=list[SubjectOut])
async def list_subjects(
    db: Annotated[AsyncSession, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> list[Subject]:
    return await subject_repository.list_all(db)
