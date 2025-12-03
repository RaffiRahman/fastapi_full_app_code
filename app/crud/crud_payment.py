from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate


def get_payment(db: Session, payment_id: int) -> Payment | None:
    return db.query(Payment).filter(Payment.id == payment_id).first()

def get_payments_by_invoice(db: Session, invoice_id: int, skip: int = 0, limit: int = 100) -> list[Payment]:
    return db.query(Payment).filter(Payment.invoice_id == invoice_id).offset(skip).limit(limit).all()

def create_payment(db: Session, payment: PaymentCreate) -> Payment:
    db_payment = Payment(**payment.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def update_payment(db: Session, payment: Payment, payment_in: PaymentUpdate) -> Payment:
    for field, value in payment_in.model_dump(exclude_unset=True).items():
        setattr(payment, field, value)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

def delete_payment(db: Session, payment: Payment):
    db.delete(payment)
    db.commit()