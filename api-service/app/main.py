from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import bearer_token_middleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.options("/{full_path:path}")
async def options_route(full_path: str):
    return {"message": "OK"}

app.include_router(api_router)
add_exception_handlers(app)

app.middleware("http")(bearer_token_middleware)
