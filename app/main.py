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
    articles,
    auth,
    carts,
    categories,
    cms,
    payments,
    products,
    reviews,
    tags,
    tools,
    uploads,
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
                   prefix=f"{settings.API_V1_STR}/auth",
                   tags=["auth"])
app.include_router(cms.router,
                   prefix=settings.API_V1_STR,
                   tags=["cms"])
app.include_router(products.router,
                   prefix=f"{settings.API_V1_STR}/products",
                   tags=["products"])
app.include_router(articles.router,
                   prefix=f"{settings.API_V1_STR}/articles",
                   tags=["articles"])
app.include_router(categories.router,
                   prefix=f"{settings.API_V1_STR}/categories",
                   tags=["categories"])
app.include_router(tags.router,
                   prefix=f"{settings.API_V1_STR}/tags",
                   tags=["tags"])
app.include_router(tools.router,
                   prefix=f"{settings.API_V1_STR}/tools",
                   tags=["tools"])
app.include_router(carts.router,
                   prefix=f"{settings.API_V1_STR}/carts",
                   tags=["carts"])
app.include_router(reviews.router,
                   prefix=f"{settings.API_V1_STR}/reviews",
                   tags=["reviews"])
app.include_router(payments.router,
                   prefix=f"{settings.API_V1_STR}/payments",
                   tags=["payments"])
app.include_router(uploads.router,
                   prefix=f"{settings.API_V1_STR}/uploads",
                   tags=["uploads"])

# Serve uploaded files
upload_path = Path(settings.UPLOAD_DIR)
upload_path.mkdir(parents=True, exist_ok=True)
upload_path.chmod(0o755)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")



