from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import crud_tag
from app.dependencies import get_current_superuser, get_db
from app.schemas.tag import Tag, TagCreate, TagUpdate

router = APIRouter()

@router.post("/", response_model=Tag, status_code=status.HTTP_201_CREATED)
def create_tag(tag: TagCreate,
               db: Session = Depends(get_db),
               current_superuser: bool = Depends(get_current_superuser)
):
    db_tag = crud_tag.get_tag_by_slug(db, slug=tag.slug)
    if db_tag:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag with this slug already exists.")
    return crud_tag.create_tag(db, tag)

@router.get("/", response_model=list[Tag])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = crud_tag.get_tags(db, skip=skip, limit=limit)
    return tags

@router.get("/{tag_id}", response_model=Tag)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = crud_tag.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag

@router.get("/slug/{slug}", response_model=Tag)
def read_tag_by_slug(slug: str, db: Session = Depends(get_db)):
    tag = crud_tag.get_tag_by_slug(db, slug=slug)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.put("/{tag_id}", response_model=Tag)
def update_tag(
    tag_id: int,
    tag_update: TagUpdate,
    db: Session = Depends(get_db),
    current_superuser: bool = Depends(get_current_superuser),
):
    db_tag = crud_tag.get_tag(db, tag_id)
    if not db_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return crud_tag.update_tag(db, db_tag, tag_update)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db), current_superuser: bool = Depends(get_current_superuser)):
    db_tag = crud_tag.get_tag(db, tag_id)
    if not db_tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    crud_tag.delete_tag(db, db_tag)
    return
