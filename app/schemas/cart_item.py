from pydantic import BaseModel

class CartItemBase(BaseModel):
    product_id: int
    quantity: int


class CartItemCreate(CartItemBase):
    pass

class CartItemUpdate(BaseModel):
    product_id: int | None = None
    quantity: int | None = None

class CartItem(CartItemBase):
    id: int
    cart_id: int

    class Config:
        from_attributes = True



