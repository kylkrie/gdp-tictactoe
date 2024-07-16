from fastapi import APIRouter
from .boards.routes import router as boards_router

router = APIRouter(prefix="/api")

router.include_router(boards_router)
