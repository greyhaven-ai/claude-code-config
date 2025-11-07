# Grey Haven Studio - Error Handler Template
# Add this to app/core/exceptions.py

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, OperationalError
import logging

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTPException with standard error format."""
    logger.warning(f"HTTP exception: {exc.status_code} - {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
        },
        headers=exc.headers,
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        field_path = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append(
            {
                "field": field_path if field_path else None,
                "message": error["msg"],
                "code": error["type"],
            }
        )

    logger.warning(f"Validation error: {errors}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "detail": errors,
            "status_code": 422,
        },
    )


async def integrity_error_handler(
    request: Request, exc: IntegrityError
) -> JSONResponse:
    """Handle database integrity errors."""
    logger.error(f"Integrity error: {exc}")

    error_detail = "A resource with this unique value already exists"
    if "foreign key" in str(exc).lower():
        error_detail = "Referenced resource does not exist"

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": error_detail,
            "status_code": 409,
        },
    )


async def operational_error_handler(
    request: Request, exc: OperationalError
) -> JSONResponse:
    """Handle database operational errors."""
    logger.error(f"Database operational error: {exc}")

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "Service temporarily unavailable",
            "detail": "Database connection error. Please try again later.",
            "status_code": 503,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unexpected exceptions."""
    logger.exception(f"Unhandled exception: {exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "status_code": 500,
        },
    )


# Register in main.py:
# from app.core.exceptions import (
#     http_exception_handler,
#     validation_exception_handler,
#     integrity_error_handler,
#     operational_error_handler,
#     generic_exception_handler,
# )
#
# app.add_exception_handler(HTTPException, http_exception_handler)
# app.add_exception_handler(RequestValidationError, validation_exception_handler)
# app.add_exception_handler(IntegrityError, integrity_error_handler)
# app.add_exception_handler(OperationalError, operational_error_handler)
# app.add_exception_handler(Exception, generic_exception_handler)
