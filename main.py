import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, IntegrityError

from app.core.logger import logger
from app.db.engine import engine
from app.exceptions.handlers import (
    operational_error_handler,
    integrity_error_handler,
    BaseApiException,
    handle_exception_response,
    handle_validation_error_handler,
)
from app.api.routers import api_router
from app.core.config import settings
from app.core.middleware.db import db_error_logger
from app.core.middleware.logging import LoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection successful")
    except (OperationalError, ConnectionRefusedError, asyncio.TimeoutError) as e:
        if settings.ENV.lower() == "prod":
            logger.error("❌ Database is not reachable, shutting down application")
            raise RuntimeError("Database connection failed") from e
        else:
            logger.warning(f"⚠️ Database is not reachable. Continuing anyway: {e}")

    yield

    await engine.dispose()
    logger.info("🛑 Database connections closed")


def create_app() -> FastAPI:
    """
    Создаёт и настраивает FastAPI приложение
    """
    app = FastAPI(docs_url="/", lifespan=lifespan)

    # Middleware
    app.add_middleware(LoggingMiddleware)
    app.middleware("http")(db_error_logger)

    # Exception handlers
    app.add_exception_handler(RequestValidationError, handle_validation_error_handler)
    app.add_exception_handler(BaseApiException, handle_exception_response)
    app.add_exception_handler(OperationalError, operational_error_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)

    # Роуты
    app.include_router(api_router)

    return app


app = create_app()


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(
        app,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        access_log=False,
    )
