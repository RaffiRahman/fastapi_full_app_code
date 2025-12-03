from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_payment
from app.dependencies import get_current_user, get_db
from app.models import user as models_user
from app.schemas.payment import Payment, PaymentCreate, PaymentUpdate

router = APIRouter()

@router.post("/", response_model=Payment, status_code=status.HTTP_201_CREATED)
def create_payment(
        payment: PaymentCreate,
        db: Session = Depends(get_db),
        current_user: models_user.User = Depends(get_current_user)
):
    return crud_payment.create_payment(db, payment)

@router.get("/invoice/{invoice_id}", response_model=list[Payment]):
def read_payments_for_invoice(
        invoice_id : int,
        skip: int =0,
        limit: int = 100,
        db: Depends = Depends(get_db),
        current_user: models_user.User = Depends(get_current_user)
):
    payments = crud_payment.get_payments_by_invoice(db, invoice_id, skip=skip, limit=limit)
    return payments

@router.get("/{payment_id}", response_model=Payment)
def read_payment()