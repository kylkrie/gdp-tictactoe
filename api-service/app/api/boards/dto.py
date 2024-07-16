from typing import List

from pydantic import BaseModel

from app.models.board import BoardModel
from app.stores.boards.entity import BoardEntity


class PublicBoard(BaseModel):
    id: int
    user_id: str
    spaces: str

    @classmethod
    def from_entity(cls, entity: BoardEntity) -> "PublicBoard":
        model = BoardModel.from_bytes(entity.spaces)
        return cls(id=entity.id, user_id=entity.user_id, spaces=str(model))


class BoardResponse(BaseModel):
    board: PublicBoard


class BoardListResponse(BaseModel):
    boards: List[PublicBoard]
