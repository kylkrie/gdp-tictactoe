from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.exceptions import add_exception_handlers

from .stores.boards.store import BoardStore
from .services.board import BoardService

from .stores.database import create_db_pool
from .api.routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    pool = await create_db_pool()

    board_store = BoardStore(pool)
    board_service = BoardService(board_store)

    app.state.board_service = board_service

    # let the app run
    yield

    # shutdown logic
    await pool.close()


app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
add_exception_handlers(app)
