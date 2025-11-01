from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ArticleBase(BaseModel):
    title: str
    slug: str
    content: str | None = None
    featured: bool | None = None
    status: str = "draft"
    tyoe: str # 'blog or 'tutorial'
    category_ids: list[int] = []
    tag_ids: list[int] = []


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: str | None = None
    slug: str | None = None
    content: str | None = None
    featured_image_url: str | None = None
    excerpt: str | None = None
    status: str | None = None
    type: str | None = None
    category_ids: list[int] | None = None
    tag_ids: list[int] | None = None


class Article(ArticleBase):
    id: int
    author_id: int | None = None
    published_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
