from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .response import error_response


class UnauthorizedException(Exception):
    pass


def add_handlers(app: FastAPI):
    app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)


async def unauthorized_exception_handler(req: Request, exc: Exception):
    return JSONResponse(
        status_code=401,
        content=error_response("Unauthorized", str(exc)),
    )
