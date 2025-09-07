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

