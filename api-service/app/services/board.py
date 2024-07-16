import random
from typing import List
from app.models.board import BoardModel
from app.stores.boards.entity import BoardEntity
from app.stores.boards.store import BoardStore


class BoardService:
    def __init__(self, board_store: BoardStore):
        self.board_store = board_store

    async def create_board(self, user_id: str) -> BoardEntity:
        model = BoardModel()
        # 50% chance player is X
        if random.random() < 0.5:
            model.make_computer_move()

        return await self.board_store.create(user_id, model)

    async def get_board(self, id: int) -> BoardEntity:
        return await self.board_store.get(id)

    async def get_boards(self, skip: int = 0, limit: int = 20) -> List[BoardEntity]:
        return await self.board_store.get_many(skip, limit)

    async def make_move(self, id: int, user_id: str, position: int) -> BoardEntity:
        entity = await self.get_board(id)
        model = BoardModel.from_bytes(entity.spaces)
        # player move
        model.make_move(position)

        # check for win
        result = model.try_get_result()

        if not result:
            # no result, make a computer move
            model.make_computer_move()

        # save new state
        return await self.board_store.update(id, user_id, model)
