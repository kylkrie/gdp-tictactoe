from enum import Enum
import random
from typing import List, Optional


class BoardPlayer(Enum):
    X = "x"
    O = "o"


class BoardResult(Enum):
    WIN_X = "win_x"
    WIN_O = "win_o"
    TIE = "tie"


class InvalidMoveException(Exception):
    pass


class BoardDeserializationException(Exception):
    pass


class BoardModel:
    def __init__(self):
        self._spaces: List[Optional[BoardPlayer]] = [None for _ in range(9)]

    def __str__(self) -> str:
        return "".join(space.value if space else "_" for space in self._spaces)

    def to_bytes(self) -> bytes:
        # each space only has 3 states, we can store each space using 2 bits
        # 00 - Empty
        # 01 - X
        # 10 - O
        # there are 9 board spaces, 9 x 2 = 18 bits, or 3 bytes
        # practically, this isn't much savings over the 9 bytes if we just used a str
        # but I thought I would show an example of optimzations I'm thinking about
        data = bytearray(3)
        for i, space in enumerate(self._spaces):
            value = 0 if space is None else (1 if space == BoardPlayer.X else 2)
            # 2 bits per space, 1 byte fits 4 spaces
            byte_index = i // 4
            bit_offset = (i % 4) * 2
            left_shifted = value << bit_offset
            # bitwise OR to set data. 00XX | YY00 = YYXX
            data[byte_index] |= left_shifted

        return data

    @classmethod
    def from_bytes(cls, data: bytes) -> "BoardModel":
        if len(data) != 3:
            raise BoardDeserializationException(
                f"Invalid data length: expected 3 bytes, got {len(data)}"
            )

        board = cls()
        for i in range(9):
            byte_index = i // 4
            bit_offset = (i % 4) * 2
            right_shifted = data[byte_index] >> bit_offset
            # bitwise AND to extract value. YYXX & 0011 = 00XX
            value = right_shifted & 0b11
            # bits 11 is an invalid state
            if value == 0b11:
                raise BoardDeserializationException(
                    f"Invalid state {value} found at board position {i}"
                )

            board._spaces[i] = (
                None if value == 0 else (BoardPlayer.X if value == 1 else BoardPlayer.O)
            )

        return board

    def get_current_player(self) -> BoardPlayer:
        x_count = self._spaces.count(BoardPlayer.X)
        o_count = self._spaces.count(BoardPlayer.O)

        # X always goes first. if the counts are the same, than its X's turn
        return BoardPlayer.X if x_count == o_count else BoardPlayer.O

    def make_move(self, position: int) -> None:
        result = self.try_get_result()
        if result:
            raise InvalidMoveException(f"Result {result} already determined")
        if not 0 <= position < 9:
            raise InvalidMoveException(
                f"Position {position} out of range (must be 0-8)"
            )
        if self._spaces[position]:
            raise InvalidMoveException(f"Position {position} already taken")

        self._spaces[position] = self.get_current_player()

    def make_computer_move(self):
        empty_positions = [i for i, space in enumerate(self._spaces) if space is None]
        if not empty_positions:
            raise InvalidMoveException("No board positions left")

        random_position = random.choice(empty_positions)
        self.make_move(random_position)

    def try_get_result(self) -> Optional[BoardResult]:
        winning_lines = [
            # rows
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            # columns
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            # diagonals
            (0, 4, 8),
            (2, 4, 6),
        ]

        for a, b, c in winning_lines:
            if (
                self._spaces[a]
                and self._spaces[a] == self._spaces[b] == self._spaces[c]
            ):
                return (
                    BoardResult.WIN_X
                    if self._spaces[a] == BoardPlayer.X
                    else BoardResult.WIN_O
                )

        if all(self._spaces):
            return BoardResult.TIE

        return None
