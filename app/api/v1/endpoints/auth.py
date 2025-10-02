from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

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


