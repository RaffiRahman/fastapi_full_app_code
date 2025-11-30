from sqlalchemy.orm import Session

from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate


def get_reviews(db: Session, review_id: int) -> Review | None:
    return db.query(Review).filter(Review.id == review_id).first()

def get_reviews_by_product(db: Session, product_id: int, skip: int = 0, limit: int = 100) -> list[Review]:
    return db.query(Review).filter(Review.product_id == product_id).offset(skip).limit(limit).all()

def create_review(db: Session, review: ReviewCreate) -> Review:
    db_review = Review(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def update_review(db: Session, review: Review, review_in: ReviewUpdate) -> Review:
    for field, value in review_in.model_dump(exclude_unset=True).items():
        setattr(review, field, value)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def delete_review(db: Session, review: Review):
    db.delete(review)
    db.commit()
