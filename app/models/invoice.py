from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Invoice(Base):
    """Invoice generated for an order."""

    __tablename__ = "invoices"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False) # my addition ----> TODO
    invoice_date = Column(DateTime(timezone=True), server_default=func.now())
    due_date = Column(DateTime(timezone=True))
    amount = Column(Float)
    status = Column(String(20))
    payment_method = Column(String(50))

    order = relationship("Order", backref="invoices")
    user = relationship("User", backref="invoices")
