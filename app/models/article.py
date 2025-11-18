from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


# Association table for articles and categories
article_categories = Table(
    "article_categories",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True),
    extend_existing=True
)

# Association table for articles and tags
article_tags = Table(
    "article_tags",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
    extend_existing=True
)

class Article(Base):
    """Blog or tutorial article."""

    __tablename__ = "articles"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20), nullable=False)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    featured_image_url = Column(String(255))
    excerpt = Column(Text)
    status = Column(String(20), nullable=False, default="draft")
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone= True), server_default=func.now(), onupdate=func.now(), nullable=False)

    author = relationship("User", backref="articles")
    categories = relationship("Category", secondary=article_categories, backref="articles")
    tags = relationship("Tag", secondary=article_tags, backref="articles")
