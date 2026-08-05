from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_role
from app.core.database import get_db
from app.models.enums import UserRole
from app.models.fee_invoice import FeeInvoice
from app.models.fee_payment import FeePayment
from app.models.user import User
from app.repositories import fee_repository
from app.schemas.fee import FeeInvoiceCreate, FeeInvoiceOut, FeePaymentCreate, FeePaymentOut
from app.services import fee_service

router = APIRouter(prefix="/fees", tags=["fees"])


@router.post("/invoices", response_model=FeeInvoiceOut, status_code=status.HTTP_201_CREATED)
async def create_invoice(
    data: FeeInvoiceCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _staff: Annotated[User, Depends(require_role(UserRole.ADMIN, UserRole.ACCOUNTANT))],
) -> FeeInvoice:
    return await fee_service.create_invoice(db, data)


@router.post("/payments", response_model=FeePaymentOut, status_code=status.HTTP_201_CREATED)
async def record_payment(
    data: FeePaymentCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    _accountant: Annotated[User, Depends(require_role(UserRole.ACCOUNTANT, UserRole.ADMIN))],
) -> FeePayment:
    return await fee_service.record_payment(db, data)


@router.get("/me", response_model=list[FeeInvoiceOut])
async def my_invoices(
    db: Annotated[AsyncSession, Depends(get_db)],
    student: Annotated[User, Depends(require_role(UserRole.STUDENT))],
) -> list[FeeInvoice]:
    return await fee_repository.list_invoices_for_student(db, student.id)
