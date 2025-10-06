import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.v1.endpoints import (
    auth,
    users,
)
from app.core.config import settings
from app.core.exceptions import (
    InvalidCredentialsError,
    PermissionDeniedError,
    TokenExpiredError,
    UserAlreadyExistsError,
)
from app.core.middleware import RequestLoggingMiddleware

logger = logging.getLogger(__name__)

# Configure logging for production
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI(
    title="Backend API Learning",
    docs_url='/docs',
    redoc_url='/redoc',
)

app.include_router(users.router,
                   prefix=f"{settings.API_V1_STR}/users",
                   tags=["users"])
app.include_router(auth.router,
                   prefix=f"{settings.API_V1_STR}/users",
                   tags=["users"])