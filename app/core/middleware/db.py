from fastapi import Request
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError


async def db_error_logger(request: Request, call_next):
    try:
        return await call_next(request)
    except SQLAlchemyError:
        logger.exception(f"Unexpected DB error on {request.url.path}")
        raise
