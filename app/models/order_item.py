from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class OrderItem(Base):
    """Line item within an order."""

    __tablename__ = 'order_items'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer)
    price_at_purchase = Column(Float)

    order = relationship('Order', backref='items')
    product = relationship('Product')
