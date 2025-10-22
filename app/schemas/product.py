from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    title: str
    slug: str
    description: str | None = None
    cover_image_url: str | None = None
    price: float
    author_name: str | None = None
    rating: float = 0.0
    language: str
    publication_date: datetime | None = None
    pages: int | None = None
    format: str | None = None
    table_of_contents: dict | None = None
    status: str = "draft"
    is_featured: bool = False
    category_ids: list[int] = []
    tag_ids: list[int] = []

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    description: str | None = None
    cover_image_url: str | None = None
    price: float | None = None
    author_name: str | None = None
    rating: float | None = None
    language: str | None = None
    publication_date: datetime | None = None
    pages: int | None = None
    format: str | None = None
    table_of_contents: dict | None = None
    status: str | None = None
    is_featured: bool | None = None
    category_ids: list[int] | None = None
    tag_ids: list[int] | None = None

class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

