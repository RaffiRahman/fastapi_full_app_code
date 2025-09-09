import time
from collections import defaultdict
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError #type: ignore
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

from app.core.config import settings
from app.core.database import get_db
from app.core.exceptions import InvalidCredentialsError
from app.core.security import verify_token
from app.crud import crud_user as crud
from app.models import user as models_user
from app.schemas import user as schemas_user

#OAuth2 scheme
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")

#rate limiting configuration
RATE_LIMIT = 5 # max requests
TIME_WINDOW = 60 # Time window in seconds
request_counts: defaultdict[str, list[float]] = defaultdict(list)

async def rate_limiter(request: Request) -> None:
    """Rate limiting dependency to prevent abouse."""
    client_ip = request.client.host if request.client else "unknown"
    current_time = time.time()
    request_times = request_counts[client_ip]

    #Remove outdated requests
    request_counts[client_ip] = [t for t in request_times if current_time - t < TIME_WINDOW]

    if len(request_counts[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=HTTP_429_TOO_MANY_REQUESTS, detail="Too many requests. Please try again later.")
    request_counts[client_ip].append(current_time)

async def get_current_user(
        token: Annotated[str, Depends(reusable_oauth2)],
        db: Session = Depends(get_db),
) -> models_user.User:
    """Retrive the current user from the JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        token_data = schemas_user.TokenData(email= payload.get("sub"))
        if not token_data.email:
            raise credentials_exception
    except (JWTError, ValidationError, InvalidCredentialsError, KeyError):
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    print(f"User {user.email} is_superuser: {user.is_superuser} ")
    return user

async def get_current_active_user(
        current_user: Annotated[models_user.User, Depends(get_current_user)],
) -> models_user.User:
    """Ensure the current user is active."""
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user.")
    return current_user

async def get_current_active_superuser(
        current_user: Annotated[models_user.User, Depends(get_current_user)],
) -> models_user.User:
    """Ensure the current user has superuser privileges."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    return current_user

async def get_current_superuser(
        current_user: Annotated[models_user.User, Depends(get_current_user)],
) -> models_user.User:
    """Alias for backward compatibility."""
    return await get_current_active_superuser(current_user)

async def get_current_active_superuser_or_user(
        current_user: Annotated[models_user.User, Depends(get_current_user)],
) -> models_user.User:
    """Return the current user regardless of privileges."""
    return current_user