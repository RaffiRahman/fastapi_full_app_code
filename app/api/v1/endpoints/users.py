from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.ip_filter import verify_admin_ip
from app.crud import crud_user as crud
from app.dependencies import get_current_active_superuser
from app.schemas import user as schemas_user

router = APIRouter(dependencies=[Depends(verify_admin_ip)])

@router.get("/", response_model=list[schemas_user.User])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: schemas_user.User = Depends(get_current_active_superuser),
):
    """
    Retrieve a list of users. Requires superuser privileges.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.post("/", response_model=schemas_user.User)
def create_user(
        user: schemas_user.UserCreate,
        db: Session = Depends(get_db),
        current_user: schemas_user.User = Depends(get_current_active_superuser),
):
    """
    Create a new user. Requires superuser privileges.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db,user=user)

@router.post("/superuser", response_model=schemas_user.User)
def create_superuser(
        user: schemas_user.UserCreate,
        db: Session = Depends(get_db),
        current_user: schemas_user.User = Depends(get_current_active_superuser),
):
    """
    Create a new superuser. Requires superuser privileges.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/{user_id}", response_model=schemas_user.User)
def read_user_by_id(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: schemas_user.User = Depends(get_current_active_superuser),
):
    """
    Retrieve a user by ID. Requires superuser privileges.
    """
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=schemas_user.User)
def update_user(
        user_id: int,
        user_in: schemas_user.UserUpdate,
        db: Session = Depends(get_db),
        current_user: schemas_user.User = Depends(get_current_active_superuser),
):
    """Update a user's information. Requires superuser privileges."""
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db, db_user=db_user, user_in=user_in)

@router.delete("/{user_id}", response_model=schemas_user.User)
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: schemas_user.User = Depends(get_current_active_superuser),
):
    """Delete a user. Requies superuser privileges."""
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, user_id= user_id)
    return {"message":"User deleted successfully"}