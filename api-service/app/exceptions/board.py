from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.models.board import InvalidMoveException
from .response import error_response


def add_handlers(app: FastAPI):
    app.add_exception_handler(InvalidMoveException, invalid_move_exception_handler)


async def invalid_move_exception_handler(req: Request, exc: InvalidMoveException):
    return JSONResponse(
        status_code=400, content=error_response("InvalidMove", str(exc))
    )
