from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.crud import crud_article
from app.dependencies import get_current_superuser, get_current_user, get_db
from app.models import user as models_user
from app.schemas.article import Article, ArticleCreate, ArticleUpdate


router = APIRouter()



@router.post("/", response_model=Article, status_code=status.HTTP_201_CREATED)
def create_article(
        article: ArticleCreate,
        db: Session = Depends(get_db),
        current_user: models_user.User = Depends(get_current_user),
):
    db_article = crud_article.get_article(db, slug= article.slug)
    if db_article:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Article with this slug already exixts")
    return crud_article.create_article(db, article, int(current_user.id))


@router.get("/", response_model=list[Article])
def read_articles(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        serach: Optional[str] = Query(None, description="Search in title and content"),
        status: Optional[str] = Query("published", description="Filter by status"),
        type: Optional[str] = Query(None, description="Filter by article type"),
        category: Optional[str] = Query(None, description="Filter by category_slug"),
        featured: Optional[bool] = Query(None, description="Filter featured articles"),
        sort_by: Optional[str] = Query("published_at", description="Sort by field"),
        sort_order: Optional[str] = Query("desc", description="Sort order (asc/desc)"),
        db: Session = Depends(get_db)
):
    articles = crud_article.get_articles(
        db=db,
        skip=skip,
        limit=limit
    )
    return articles

@router.put("/{slug}", response_model=Article)
def update_article(
        slug: str,
        article_update: ArticleUpdate,
        db: Session = Depends(get_db),
        current_user: models_user.User = Depends(get_current_user),
):
    db_article = crud_article.get_article(db, slug=slug)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

    # Only allow superusers or the author to update the article
    if not current_user.is_superuser and db_article.author_id != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this article")

    return crud_article.update_article(db, db_article, article_update)


@router.delete("/{slug}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(slug: str, db: Session = Depends(get_db), current_superuser: bool = Depends(get_current_superuser)):
    db_article = crud_article.get_article(db, slug=slug)
    if not db_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    crud_article.delete_article(db, db_article.id)
    return