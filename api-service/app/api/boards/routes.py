from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from .dto import BoardListResponse, BoardResponse, PublicBoard
from app.services.board import BoardService

router = APIRouter(prefix="/boards/v1")


def get_board_service(req: Request) -> BoardService:
    return req.app.state.board_service


####################
## Create


@router.post("", response_model=BoardResponse)
async def create_board(board_service: BoardService = Depends(get_board_service)):
    user_id = "test"
    board_entity = await board_service.create_board(user_id)

    return BoardResponse(board=PublicBoard.from_entity(board_entity))


####################
## Get Many


@router.get("", response_model=BoardListResponse)
async def get_boards(board_service: BoardService = Depends(get_board_service)):
    board_entities = await board_service.get_boards()

    public_boards = [PublicBoard.from_entity(entity) for entity in board_entities]

    return BoardListResponse(boards=public_boards)


####################
## Get One


@router.get("/{id}", response_model=BoardResponse)
async def get_board(id: int, board_service: BoardService = Depends(get_board_service)):
    board_entity = await board_service.get_board(id)
    if board_entity is None:
        raise HTTPException(status_code=404, detail="Board not found")

    return BoardResponse(board=PublicBoard.from_entity(board_entity))


####################
## Make Move


class MakeMoveBody(BaseModel):
    position: int


@router.post("/{id}/move", response_model=BoardResponse)
async def get_board(
    id: int,
    body: MakeMoveBody,
    board_service: BoardService = Depends(get_board_service),
):
    user_id = "test"
    board_entity = await board_service.make_move(id, user_id, body.position)

    return BoardResponse(board=PublicBoard.from_entity(board_entity))
