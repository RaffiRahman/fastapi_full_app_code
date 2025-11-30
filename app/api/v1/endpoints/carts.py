from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_cart,crud_product
from app.dependencies import get_current_user, get_db
from app.models import user as models_user
from app.schemas.cart import Cart, CartCreate
from app.schemas.cart_item import CartItem, CartItemCreate, CartItemUpdate


router = APIRouter()

@router.get("/me", response_model=Cart)
def read_my_cart(db: Session = Depends(get_db), current_user: models_user.User = Depends(get_current_user)):
    cart = crud_cart.get_cart_by_user_id(db, user_id=int(current_user.id))
    if not cart:
        # Create a cart if it doesn't exist for the user
        cart = crud_cart.create_cart(db, CartCreate(user_id=int(current_user.id)))
    return cart


@router.post("/items", response_model=CartItem, status_code=status.HTTP_201_CREATED)
def add_item_to_cart(
    item: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: models_user.User = Depends(get_current_user),
):
    cart = crud_cart.get_cart_by_user_id(db, user_id=int(current_user.id))
    if not cart:
        cart = crud_cart.create_cart(db, CartCreate(user_id=int(current_user.id)))

    # Check if product exists
    product = crud_product.get_product(db, item.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Check if item already in cart, then update quantity
    for existing_item in cart.items:
        if existing_item.product_id == item.product_id:
            updated_quantity = existing_item.quantity + item.quantity
            return crud_cart.update_cart_item(db, existing_item, CartItemUpdate(quantity=updated_quantity))

    return crud_cart.create_cart_item(db, item, int(cart.id))


@router.put("/items/{item_id}", response_model=CartItem)
def update_cart_item_quantity(
    item_id: int,
    item_update: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: models_user.User = Depends(get_current_user),
):
    cart = crud_cart.get_cart_by_user_id(db, user_id=int(current_user.id))
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

    db_item = crud_cart.get_cart_item(db, item_id)
    if not db_item or db_item.cart_id != cart.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    if item_update.quantity is None or item_update.quantity <= 0:
        crud_cart.delete_cart_item(db, db_item)
        return {"message": "Item removed from cart"}

    return crud_cart.update_cart_item(db, db_item, item_update)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models_user.User = Depends(get_current_user),
):
    cart = crud_cart.get_cart_by_user_id(db, user_id=int(current_user.id))
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

    db_item = crud_cart.get_cart_item(db, item_id)
    if not db_item or db_item.cart_id != cart.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart item not found")

    crud_cart.delete_cart_item(db, db_item)
    return
