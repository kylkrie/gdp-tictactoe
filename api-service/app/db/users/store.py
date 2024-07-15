from typing import List, Optional
from asyncpg import Pool
from fastapi import Request
from .entity import UserCreate, UserEntity

class UserStore:
  def __init__(self, pool: Pool):
    self.pool = pool

  async def create_user(self, data: UserCreate) -> UserEntity:
    async with self.pool.acquire() as conn:
      query = """
        INSERT INTO users (name)
        VALUES ($1)
        RETURNING *
      """
      row = await conn.fetchrow(query, data.name)
      return UserEntity.model_validate(dict(row))

  async def get_user(self, id: int) -> Optional[UserEntity]:
    async with self.pool.acquire() as conn:
      query = """
        SELECT *
        FROM users
        WHERE id = $1
      """
      row = await conn.fetchrow(query, id)
      return UserEntity.model_validate(dict(row)) if row else None

  async def get_users(self, skip: int = 0, limit: int = 20) -> List[UserEntity]:
      async with self.pool.acquire() as conn:
        query = """
          SELECT *
          FROM users
          ORDER BY created_at DESC
          LIMIT $1 OFFSET $2
        """
        rows = await conn.fetch(query, limit, skip)
        return [UserEntity.model_validate(dict(row)) for row in rows]
