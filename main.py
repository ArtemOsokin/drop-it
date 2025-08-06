from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.exceptions.http_exceptions import (
    BaseApiException,
    handle_exception_response,
    handle_validation_error_handler,
)
from app.api.routers import api_router
from app.core.config import settings
from app.middleware.logging import LoggingMiddleware



def create_app() -> FastAPI:
    """
    Создаёт и настраивает FastAPI приложение
    """

    app = FastAPI(docs_url="/")

    app.add_middleware(LoggingMiddleware)

    app.add_exception_handler(RequestValidationError, handle_validation_error_handler)
    app.add_exception_handler(BaseApiException, handle_exception_response)

    app.include_router(api_router)

    return app


app = create_app()


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT, access_log=False)
