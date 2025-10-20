from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base

class MenuItem(Base):
    """Individual menu item."""

    __tablename__ = "menu_items"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    title = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    parent_id = Column(Integer, ForeignKey("menu_items.id"))
    order = Column(Integer, nullable=False, default=0)

    menu = relationship("Menu", backref="items")
    parent = relationship("MenuItem", remote_side=[id], backref="children")
