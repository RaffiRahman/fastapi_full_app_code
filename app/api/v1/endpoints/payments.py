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

@router.get("/invoice/{invoice_id}", response_model=list[Payment])
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
def read_payment(
        payment_id: int,
        db: Session = Depends(get_db),
        current_user: models_user.User = Depends(get_current_user)
):
    payment = crud_payment.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    # TODO: Add logic to check if payment's invoice belongs to current_user or if current_user is admin
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this payment"
        )
    if payment.invoice and payment.invoice.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this payment"
        )
    return payment


@router.put("/{payment_id}", response_model=Payment)
def update_payment(
        payment_id: int,
        payment_update: PaymentUpdate,
        db: Session = Depends(get_db),
        current_user: models_user.User = Depends(get_current_user)
):
    db_payment = crud_payment.get_payment(db, payment_id)
    if not db_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    # TODO: Add logic to check if payment's invoice belongs to current_user or if current_user is admin
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this payment"
        )
    if db_payment.invoice and db_payment.invoice.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this payment"
        )
    return crud_payment.update_payment(db, db_payment, payment_update)

@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(
        payment_id: int,
        db: Session = Depends(get_db),
        current_user: models_user.User = Depends(get_current_user)
):
    db_payment = crud_payment.get_payment(db, payment_id)
    if not db_payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Payment not found")
    # TODO: Add logic to check if payment's invoice belongs to current_user or if current_user is admin
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this payment"
        )
    if db_payment.invoice and db_payment.invoice.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this payment"
        )

    crud_payment.delete_payment(db, db_payment)
    return