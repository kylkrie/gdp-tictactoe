from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
  name: str

class UserCreate(UserBase):
  pass

class UserEntity(UserBase):
  id: int
  created_at: datetime
  updated_at: datetime
