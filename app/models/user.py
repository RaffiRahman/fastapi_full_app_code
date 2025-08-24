from sqlalchemy import Boolean, Column, Integer, String

from app.core.database import Base

class User(Base):
    """SQLALchemy model for users"""

    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index= True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    roles = Column(String, default="user")
    refresh_token = Column(String, nullable=True)
