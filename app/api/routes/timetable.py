import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_role
from app.core.database import get_db
from app.models.enums import UserRole
from app.models.timetable_entry import TimetableEntry
from app.models.user import User
from app.repositories import timetable_repository
from app.schemas.timetable import TimetableEntryCreate, TimetableEntryOut
from app.services import timetable_service

router = APIRouter(prefix="/timetable", tags=["timetable"])


@router.post("", response_model=TimetableEntryOut, status_code=status.HTTP_201_CREATED)
async def create_entry(
    data: TimetableEntryCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _admin: Annotated[User, Depends(require_role(UserRole.ADMIN))],
) -> TimetableEntry:
    return await timetable_service.create_entry(db, data)


@router.get("/section/{section}", response_model=list[TimetableEntryOut])
async def get_section_timetable(
    section: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> list[TimetableEntry]:
    return await timetable_repository.list_by_section(db, section)


@router.get("/faculty/{faculty_id}", response_model=list[TimetableEntryOut])
async def get_faculty_timetable(
    faculty_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    _current_user: Annotated[User, Depends(get_current_user)],
) -> list[TimetableEntry]:
    return await timetable_repository.list_by_faculty(db, faculty_id)
