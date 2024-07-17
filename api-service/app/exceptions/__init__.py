from fastapi import FastAPI

from .db import add_handlers as add_db_handlers
from .board import add_handlers as add_board_handlers
from .unexpected import add_handlers as add_unexpected_handlers
from .auth import add_handlers as add_auth_handlers


def add_exception_handlers(app: FastAPI):
    add_db_handlers(app)
    add_board_handlers(app)
    add_unexpected_handlers(app)
    add_auth_handlers(app)
