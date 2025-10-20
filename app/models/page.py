from sqlalchemy import JSON, Column, Integer, String, Text

from app.core.database import Base


class Page(Base):
    """Static page content."""

    __tablename__ = "pages"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    subtitle = Column(Text)
    body = Column(Text)
    language = Column(String(10), nullable=False)
    seo_meta = Column(JSON)

