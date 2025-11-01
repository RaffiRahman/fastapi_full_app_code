from sqlalchemy.orm import Session
from typing import List, Optional

from app.models import article as models
from app.schemas import article as schemas
from app.models.category import Category
from app.models.tag import Tag


def get_article(db: Session, slug: str):
    return db.query(models.Article).filter(models.Article.slug == slug).first()


def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).offset(skip).limit(limit).all()


def create_article(db: Session, article: schemas.ArticleCreate, user_id: int):
    article_data = article.model_dump(exclude_unset=True)
    category_ids = article_data.pop("category_ids", [])
    tag_ids = article_data.pop("tag_ids", [])

    db_article = models.Article(**article_data, author_id=user_id)

    for category_id in category_ids:
        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            db_article.categories.append(category)

    for tag_id in tag_ids:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if tag:
            db_article.tags.append(tag)

    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(db: Session, db_article: models.Article, article_in: schemas.ArticleUpdate):
    update_data = article_in.model_dump(exclude_unset=True)

