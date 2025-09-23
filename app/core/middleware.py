import logging
import time
import uuid
from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

# Configure logging
logging.bacisConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(meaasge)s")
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app: ASGIApp,
    ) -> None:
        super().__init__(app)

    async def dispatch(
            self,
            request: Request,
            call_next: Callable
    ) -> Response:
        request_id = str(uuid.uuid4())
        start_time = time.time()

        # Log request
        client_host = request.client.host if request.client else "unknown"
        logger.info(
            f"Request started - ID: {request_id} - Method: {request.method} - "
            f"Path: {request.url.path} - Client: {client_host}"
        )

        try:
            response = await call_next(request)

            # Log response
            process_time = time.time() - start_time
            logger.info(
                f"Request completed - ID: {request_id} - Status: {response.status_code} - "
                f"Duration: {process_time:.3f}s"
            )

            # Add custom headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as e:
            logger.error(f"Request failed - ID: {request_id} - Error: {str(e)}")
            raise

