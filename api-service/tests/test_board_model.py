import pytest
from app.models.board import (
    BoardModel,
    BoardPlayer,
    BoardResult,
    InvalidMoveException,
    BoardDeserializationException,
)

# X X X
# O O _
# _ _ _
moves_win_x = [0, 3, 1, 4, 2]

# X X _
# O O O
# X _ _
moves_win_o = [0, 3, 1, 4, 6, 5]

# O X X
# X X O
# O O X
moves_tie = [4, 0, 1, 7, 2, 6, 3, 5, 8]


@pytest.fixture
def board():
    return BoardModel()


def test_initial_board_state(board):
    assert str(board) == "_________"


def test_make_move(board):
    assert board.get_current_player() == BoardPlayer.X
    board.make_move(0)
    assert str(board) == "x________"

    assert board.get_current_player() == BoardPlayer.O
    board.make_move(4)
    assert str(board) == "x___o____"

    assert board.get_current_player() == BoardPlayer.X


def test_invalid_move(board):
    # out of range
    with pytest.raises(InvalidMoveException):
        board.make_move(10)

    # position taken
    board.make_move(0)
    with pytest.raises(InvalidMoveException):
        board.make_move(0)

    # result already determined
    board.make_move(4)
    board.make_move(1)
    board.make_move(5)
    board.make_move(2)
    with pytest.raises(InvalidMoveException):
        board.make_move(6)


def test_computer_move(board):
    board.make_computer_move()
    assert str(board).count("x") == 1
    assert str(board).count("o") == 0

    board.make_computer_move()
    assert str(board).count("x") == 1
    assert str(board).count("o") == 1


def test_invalid_computer_move(board):
    for move in moves_tie:
        board.make_move(move)
    # test invalid move (needs full board)
    with pytest.raises(InvalidMoveException):
        board.make_computer_move()


def test_get_result_win_x(board):
    for move in moves_win_x:
        board.make_move(move)
    assert board.try_get_result() == BoardResult.WIN_X


def test_get_result_win_o(board):
    for move in moves_win_o:
        board.make_move(move)
    assert board.try_get_result() == BoardResult.WIN_O


def test_get_result_tie(board):
    for move in moves_tie:
        board.make_move(move)
    assert board.try_get_result() == BoardResult.TIE


def test_serialization(board):
    board.make_move(0)
    board.make_move(4)
    serialized = board.to_bytes()
    assert len(serialized) == 3
    assert serialized[0] == 0b01
    assert serialized[1] == 0b10
    assert serialized[2] == 0
    deserialized = BoardModel.from_bytes(serialized)
    assert str(board) == str(deserialized)


def test_deserialization_error():
    # invalid length
    serialized = [0b10, 0b01]
    with pytest.raises(BoardDeserializationException):
        BoardModel.from_bytes(serialized)

    # invalid space state (11)
    serialized = [0b11, 0b01, 0b10]
    with pytest.raises(BoardDeserializationException):
        BoardModel.from_bytes(serialized)
