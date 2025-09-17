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
    users
)
from app.core.config import settings
from app.core.exceptions import (
    InvalidCredentialsError,
    PermissionDeniedError,
    TokenExpiredError,
    UserAlreadyExistsError,
)
from app.core.middleware import