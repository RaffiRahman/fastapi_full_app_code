from datetime import datetime

from pydantic import BaseModel


class ReviewBase(BaseModel):
    product_id: int
    user_id: int
    rating: int
    comment: str | None = None

class ReviewCreate(ReviewBase):
    pass

class ReviewUpdate(BaseModel):
    product_id : int | None = None
    user_id: int | None = None
    rating: int | None = None
    comment: str | None = None

class Review(ReviewBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

