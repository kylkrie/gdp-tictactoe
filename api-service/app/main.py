from contextlib import asynccontextmanager
from fastapi import FastAPI

from .db.users.store import UserStore
from .services.user_service import UserService

from .db.database import create_db_pool
from .api.routes import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    pool = await create_db_pool()

    user_store = UserStore(pool)
    user_service = UserService(user_store)

    app.state.user_service = user_service
    
    # let the app run
    yield
    
    # shutdown logic
    await pool.close()

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)
