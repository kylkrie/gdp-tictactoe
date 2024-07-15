
from typing import List
from app.db.users.entity import UserCreate, UserEntity
from app.db.users.store import UserStore

class UserService:
  def __init__(self, user_store: UserStore):
    self.user_store = user_store

  async def create_user(self, name: str) -> UserEntity:
    return await self.user_store.create_user(UserCreate(name=name))

  async def get_user(self, id: int) -> UserEntity:
    return await self.user_store.get_user(id)

  async def get_users(self, skip: int = 0, limit: int = 20) -> List[UserEntity]: 
    return await self.user_store.get_users(skip, limit)
