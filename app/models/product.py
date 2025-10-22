from sqlalchemy import JSON, Boolean, Column, Date, DateTime, Float, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

# Association table for products and categories
product_categories = Table(
    "product_categories",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
    extend_existing=True
)

# Association table for products and tags
product_tags = Table(
    "product_tags",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
    extend_existing=True
)

class Product(Base):
    """Model representing eBook products."""

    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    cover_image_url = Column(String(255))
    price = Column(Float, nullable=False, default=0.0)
    author_name = Column(String(100))
    rating = Column(Float, default=0.0)
    language = Column(String(10), nullable=False)
    publication_date = Column(Date)
    pages = Column(Integer)
    format = Column(String(20))
    table_of_contents = Column(JSON)
    status = Column(String(20), nullable=False, default="draft")
    is_featured = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)


    categories = relationship("Category", secondary=product_categories, backref="products")
    tags = relationship("Tag", secondary=product_tags, backref= "products")


