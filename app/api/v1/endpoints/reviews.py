from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_product, crud_review
from app.dependencies import get_current_user, get_db
from app.models import user as models_user
from app.schemas.review import Review, ReviewCreate, ReviewUpdate

router = APIRouter()

@router.post("/", response_model=Review, status_code=status.HTTP_201_CREATED)
def create_review(
        review: ReviewCreate,
        db: Session = Depends(get_db),
        current_user: models_user.User = Depends(get_current_user)
):
    # Ensure the product exists
    product = crud_product.get_product(db, review.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    # Allow superusers to create reviews for any user
    if not current_user.is_superuser and review.user_id != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create review for this user."
        )

    return crud_review.create_review(db, review)


@router.get("/product/{product_id}", response_model=list[Review])
def read_reviews_for_product(product_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    reviews = crud_review.get_reviews_by_product(db, product_id, skip=skip, limit=limit)
    return reviews


@router.get("/{review_id}", response_model=Review)
def read_review(review_id: int, db: Session = Depends(get_db)):
    review = crud_review.get_reviews(db, review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review

@router.put("/{review_id}", response_model=Review)
def update_review(
    review_id: int,
    review_update: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: models_user.User = Depends(get_current_user),
):
    db_review = crud_review.get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    if not current_user.is_superuser and db_review.user_id != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this review",
        )

    return crud_review.update_review(db, db_review, review_update)


@router.delete("/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: models_user.User = Depends(get_current_user),
):
    db_review = crud_review.get_reviews(db, review_id)
    if not db_review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    if not current_user.is_superuser and db_review.user_id != int(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this review",
        )

    crud_review.delete_review(db, db_review)
    return


