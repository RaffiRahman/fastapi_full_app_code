from datetime import datetime

from pydantic import BaseModel


class PaymentBase(BaseModel):
    invoice_id: int
    amount_paid: float
    transaction_id: str | None = None
    payment_gateway: str | None = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    invoice_id: int | None = None
    amount_paid: float | None = None
    transaction_id: str | None = None
    payment_gateway: str | None = None


class Payment(PaymentBase):
    id: int
    payment_date: datetime

    class Config:
        from_attributes = True
