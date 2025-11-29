from sqlalchemy.orm import Session

from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.schemas.cart import CartCreate
from app.schemas.cart_item import CartItemCreate, CartItemUpdate


def get_cart_by_user_id(db: Session, user_id: int) -> Cart | None:
    return db.query(Cart).filter(Cart.user_id == user_id).first()

def create_cart(db: Session, cart: CartCreate) -> Cart:
    db_cart = Cart(**cart.model_dump())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def get_cart_item(db: Session, cart_item_id: int) -> CartItem | None:
    return db.query(CartItem).filter(CartItem.id == cart_item_id).first()

def create_cart_item(db: Session, cart_item: CartItemCreate, cart_id: int) -> CartItem:
    db_cart_item = CartItem(**cart_item.model_dump(), cart_id=cart_id)
    db.add(db_cart_item)
    db.commit()
    db.refresh(db_cart_item)
    return db_cart_item

def update_cart_item(db: Session, cart_item: CartItem, cart_item_in: CartItemUpdate) -> CartItem:
    for field, value in cart_item_in.model_dump(exclude_unset=True).items():
        setattr(cart_item, field, value)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

def delete_cart_item(db: Session, cart_item: CartItem):
    db.delete(cart_item)
    db.commit()




