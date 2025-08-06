from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.exceptions.http_exceptions import (
    BaseApiException, handle_exception_response,
    handle_validation_error_handler)
from app.api.routers import api_router
from app.middleware.logging import LoggingMiddleware

app = FastAPI(docs_url='/')

app.add_exception_handler(RequestValidationError, handle_validation_error_handler)
app.add_exception_handler(BaseApiException, handle_exception_response)
app.add_middleware(LoggingMiddleware)
app.include_router(api_router)


if __name__ == '__main__':  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host='localhost', port=32165)
