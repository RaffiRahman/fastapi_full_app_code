from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Order(Base):
    """Customer order for products."""

    __tablename__ = "orders"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    total_amount = Column(Float)
    status = Column(String(20))
    shipping_address = Column(JSON)
    billing_address = Column(JSON)

    user = relationship("User", backref="orders")
