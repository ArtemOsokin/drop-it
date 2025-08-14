import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()

        try:
            response = await call_next(request)
        except Exception as exc:
            logger.error(f"❌ Exception on {request.method} {request.url} — {exc}")
            raise

        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"{request.method} {request.url} — {response.status_code} " f"({process_time:.2f} ms)"
        )

        return response
