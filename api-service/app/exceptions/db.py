from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .response import error_response


def add_handlers(app: FastAPI):
    app.add_exception_handler(ItemNotFoundException, item_not_found_exception_handler)


class ItemNotFoundException(Exception):
    def __init__(self, item: str, id: int):
        self.item = item
        super().__init__(f"{item} not found for id: {id}")


async def item_not_found_exception_handler(req: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=404, content=error_response("ItemNotFound", str(exc))
    )
