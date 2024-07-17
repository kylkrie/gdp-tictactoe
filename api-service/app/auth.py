import os
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

from app.exceptions.auth import UnauthorizedException
from app.exceptions.response import error_response

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise ValueError("JWT_SECRET environment variable is not set")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
if not JWT_ALGORITHM:
    raise ValueError("JWT_ALGORITHM environment variable is not set")

security = HTTPBearer()


async def get_user_id(req: Request) -> str:
    user_id = req.state.user_id
    if not user_id:
        raise UnauthorizedException("User not found")

    return user_id


async def bearer_token_middleware(req: Request, call_next):
    if req.method == "OPTIONS":
        return await call_next(req)

    try:
        token = await security(req)
        if token is None:
            raise UnauthorizedException("Bearer token missing")

        payload = jwt.decode(token.credentials, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        sub = payload.get("sub")
        if not sub:
            raise UnauthorizedException("Invalid token payload")

        req.state.user_id = sub
        return await call_next(req)
    except (JWTError, UnauthorizedException, HTTPException) as e:
        return JSONResponse(
            status_code=401, content=error_response("Unauthorized", str(e))
        )
