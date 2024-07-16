from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .response import error_response


def add_handlers(app: FastAPI):
    app.add_exception_handler(Exception, unexpected_exception_handler)


async def unexpected_exception_handler(req: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=error_response(
            "InternalServiceError", "An unexpected error has occured."
        ),
    )
