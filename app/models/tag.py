from sqlalchemy import Column, Integer, String

from app.core.database import Base


class Tag(Base):
    """Simple tag for categorizing content."""

    __tablename__ = "tags"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)