from pydantic import BaseModel
from datetime import datetime


class BoardEntity(BaseModel):
    id: int
    user_id: str
    spaces: bytes
    created_at: datetime
    updated_at: datetime
