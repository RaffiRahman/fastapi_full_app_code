from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_user

from app.core.database import get_db
from app.core.exceptions import TokenExpiredError
from app.core.security import (
    create_tokens,
    send_email,
    token_blacklist,
    validate_password_complexity,
    verify_token,
    verify_password,
)
from app.crud import crud_reset_token
from app.crud import crud_user as crud
from app.dependencies import get_current_active_user, rate_limiter, reusable_oauth2
from app.models import user as models_user
from app.schemas import user as schemas_user

router = APIRouter()


@router.post("/token", response_model=schemas_user.Token, dependencies=[Depends(rate_limiter)])
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db),
):
    """OAuth2 token endpoint for user login."""
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    access_token, refresh_token = create_tokens(
        {
            "sub": user.email,
            "roles": user.roles,
            "is_superuser": user.is_superuser
        }
    )
    user.refresh_token = refresh_token
    db.add(user)
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/register", response_model=schemas_user.User)
async def register(
        user_in: schemas_user.UserCreate,
        db: Session = Depends(get_db),
):
    """Register a new user."""
    if crud.get_user_by_email(db, email= user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    try:
        user = crud.create_user(db=db, user=user_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return user

@router.post("/forgot-password")
def forgot_password(
        email_data: schemas_user.UserEmail,
        db: Session = Depends(get_db),
):
    """Send a password reset email to a user."""
    user = crud.get_user_by_email(db, email=email_data.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    token = crud_reset_token.create_password_reset_token(db, user)
    send_email(
        to=user.email,
        subject="Password reset for your account",
        body=f"Use this token to reset your password: {token}",
    )
    return {"message": "Password reset email sent"}

@router.post("/reset-password")
def reset_password(
        reset_data: schemas_user.UserPasswordReset,
        db: Session = Depends(get_db),
):
    """Reset a user's password using a token."""
    try:
        validate_password_complexity(reset_data.new_password)
        user = crud_reset_token.verify_password_reset_token(db, reset_data.token)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
        crud.update_user(
            db,
            db_user=user,
            user_in=schemas_user.UserUpdate(email=str(user.email), password=reset_data.new_password),
        )
        crud_reset_token.delete_password_reset_token(db, reset_data.token)
        return {"message": "Password reset successful"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/change-password")
def change_password(
        password_data: schemas_user.UserPasswordReset,
        current_user: models_user.User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
):
    """Change the current user's password."""
    if not verify_password(password_data.current_password, str(current_user.hashed_password)):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid current password")
    try:
        validate_password_complexity(password_data.new_password)
        crud.update_user(
            db,
            db_user=current_user,
            user_in=schemas_user.UserUpdate(email=str(current_user.email), password=password_data.new_password),
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"message": "Password updated successful"}

@router.get("/profile", response_model=schemas_user.User)
async def read_user_profile(
        curreent_user: models_user.User = Depends(get_current_active_user),
):
    """Retrieve the current user's profile."""
    return current_user

@router.put("/profile", response_model=schemas_user.User)
def update_user_profile(
        user_in: schemas_user.UserUpdate,
        db: Session = Depends(get_db),
        current_user: models_user.User = Depends(get_current_active_user),
):
    """Update current authenticated user's profile."""
    user = crud.update_user(db, db_user=current_user, user_in=user_in)
    return user

@router.post("/token/refresh", response_model=schemas_user.Token)
async def refresh_access_token(
        refresh_date: schemas_user.RefreshTokenRequest,
        token: Annotated[str, Depends(reusable_oauth2)],
        db: Session = Depends(get_db),
        current_user: models_user.User = Depends(get_current_active_user)
):
    """Refresh the access token for an authenticated user."""
    if refresh_date.refresh_token != str(current_user.refresh_token):
        raise TokenExpiredError("Unable to refresh token.")

    access_token, refresh_token = create_tokens(
        {"sub": current_user.email, "roles": current_user.roles, "is_superuser": current_user.is_superuser}
    )
    current_user.refresh_token = refresh_token   # type: ignore[assignment]
    db.add(current_user)
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(
        token: Annotated[str, Depends(reusable_oauth2)],
        db: Session = Depends(get_db),
        current_user: models_user.User = Depends(get_current_active_user)
):
    """Revoke the current user's tokens."""
    payload = verify_token(token)
    exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    token_blacklist.add_to_blacklist(payload.get("jti", ""), exp)
    current_user.refresh_token = None   # type: ignore[assignment]
    db.add(current_user)
    db.commit()
    return {"message": "Logout successful"}