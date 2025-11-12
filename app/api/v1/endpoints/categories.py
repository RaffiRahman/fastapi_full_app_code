from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_category
from app.dependencies import get_current_superuser, get_db
from app.schemas.category import Category, CategoryCreate, CategoryUpdate

router = APIRouter()


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
        category: CategoryCreate,
        db: Session = Depends(get_db),
        current_superuser: bool = Depends(get_current_superuser)
):
    db_category = crud_category.get_category_by_slug(db, slug=category.slug)
    if db_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Categry with this slug already exists")
    return crud_category.create_category(db, category)

@router.get("/", response_model=list[Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = crud_category.get_categories(db, skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = crud_category.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

@router.get("/slug/{slug}", response_model=Category)
def read_category_by_slug(slug: str, db: Session = Depends(get_db)):
    category = crud_category.get_category_by_slug(db, slug=slug)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=Category)
def update_category(
        category_id: int,
        category_update: CategoryUpdate,
        db: Session = Depends(get_db),
        current_superuser: bool = Depends(get_current_superuser),
):
    db_category = crud_category.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return crud_category.update_category(db, db_category, category_update)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
        category_id: int,
        db: Session = Depends(get_db),
        current_superuser: bool = Depends(get_current_superuser),
):
    db_category = crud_category.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    crud_category.delete_category(db, db_category)
    return


