from sqlalchemy import Column, String, Text

from app.core.database import Base


class SiteSetting(Base):
    """Key/value site configuration."""

    __tablename__ = "site_settings"
    __table_args__ = {'extend_existing': True}

    key = Column(String(100), primary_key=True, index=True)
    value = Column(Text)