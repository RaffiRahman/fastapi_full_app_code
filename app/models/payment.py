from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Payment(Base):
    """Payment record for an invoice."""

    __tablename__ = "payments"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    payment_date = Column(DateTime(timezone=True),server_default=func.now())
    amount_paid = Column(Float)
    transaction_id = Column(String(100))
    payment_gateway = Column(String(100))

    invoice = relationship("Invoice", backref="payments")