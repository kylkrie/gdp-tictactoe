from typing import List, Optional
from asyncpg import Pool

from app.models.board import BoardModel
from .entity import BoardEntity


class BoardStore:
    def __init__(self, pool: Pool):
        self.pool = pool

    async def create(self, user_id: str, board: BoardModel) -> BoardEntity:
        spaces = board.to_bytes()
        async with self.pool.acquire() as conn:
            query = """
                INSERT INTO boards (user_id, spaces)
                VALUES ($1, $2)
                RETURNING *
            """
            row = await conn.fetchrow(query, user_id, spaces)
            return BoardEntity.model_validate(dict(row))

    async def update(self, id: int, user_id: str, board: BoardModel) -> BoardEntity:
        spaces = board.to_bytes()
        async with self.pool.acquire() as conn:
            query = """
                UPDATE boards
                SET spaces = $3
                WHERE id = $1 AND user_id = $2
                RETURNING *
            """
            row = await conn.fetchrow(query, id, user_id, spaces)
            return BoardEntity.model_validate(dict(row))

    async def get(self, id: int) -> Optional[BoardEntity]:
        async with self.pool.acquire() as conn:
            query = """
                SELECT *
                FROM boards
                WHERE id = $1
            """
            row = await conn.fetchrow(query, id)
            return BoardEntity.model_validate(dict(row)) if row else None

    async def get_many(self, skip: int = 0, limit: int = 20) -> List[BoardEntity]:
        async with self.pool.acquire() as conn:
            query = """
                SELECT *
                FROM boards
                ORDER BY created_at DESC
                LIMIT $1 OFFSET $2
            """
            rows = await conn.fetch(query, limit, skip)
            return [BoardEntity.model_validate(dict(row)) for row in rows]
