from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Review(Base):
    """Product review by a user."""

    __tablename__ = 'reviews'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    product = relationship("Product", backref="reviews")