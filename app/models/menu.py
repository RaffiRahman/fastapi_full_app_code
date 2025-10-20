from sqlalchemy import Column, Integer, String

from app.core.database import Base

class Menu(Base):
    """Navigation menu container."""

    __tablename__ = "menus"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    location_slug = Column(String(100), unique=True, nullable=False)