from sqlalchemy.orm import Session

from app.core import security
from app.models import user as models
from app.schemas import user as schemas

def get_user(db: Session, user_id: int):
    """Retrieve a user by their ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Retrieve a user by their email address."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_email_with_password(db: Session, email: str):
    """Retrieve a user by their email address, including hashed password."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all users."""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user with validation."""
    # Check for existing email
    if get_user_by_email(db, email=user.email):
        raise ValueError("Email already registered")

    # Check for existing mobile number if provided
    try:
        security.validate_password_complexity(user.password)
        hashed_password = security.get_password_hash(user.password)
        db_user = models.User(
            email=user.email,
            hashed_password=hashed_password,
            name=user.name,
            is_superuser=getattr(user, "is_superuser", False),
            roles=getattr(user, "roles", "user"),
            is_active=getattr(user, "is_active", True),
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise ValueError(f"Error creatinguser: {str(e)}")

def update_user(db: Session, db_user: models.User, user_in: schemas.UserUpdate):
    """Update an existing user."""
    user_data = user_in.model_dump(exclude_unset=True)
    if "password" in user_data:
        user_data["hashes_password"] = security.get_password_hash(user_data["password"])
        del user_data["password"]

    for field in user_data:
        setattr(db_user, field, user_data[field])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """Delete a user by their ID."""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    else:
        raise ValueError("User not found")