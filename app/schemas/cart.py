from datetime import datetime

from pydantic import BaseModel

from app.schemas.cart_item import CartItem


class CartBase(BaseModel):
    user_id: int

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    id: int
    created_at: datetime
    items: list[CartItem] = []

    class Config:
        from_attributes = True

