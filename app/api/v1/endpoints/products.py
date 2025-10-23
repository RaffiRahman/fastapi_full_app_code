from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud import crud_product as crud
from app.dependencies import get_current_active_superuser
from  app.schemas import product as schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.Product])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve a list of products."""
    return crud.get_products(db, skip=skip, limit=limit)

@router.get("/{slug}", response_model=schemas.Product)
def get_product(slug: str, db: Session = Depends(get_db)):
    """Retrieve a single product by slug."""
    product = crud.get_product(db, slug=slug)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
def create_product(
        product_in: schemas.ProductCreate,
        db: Session = Depends(get_db),
        current_user= Depends(get_current_active_superuser)
):
    """Create a new product. Requires superuser."""
    return crud.create_product(db, product_in)

