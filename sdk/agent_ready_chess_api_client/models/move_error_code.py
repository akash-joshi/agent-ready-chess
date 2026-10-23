from enum import StrEnum

class MoveErrorCode(StrEnum):
    CASTLING_THROUGH_CHECK = "CASTLING_THROUGH_CHECK"
    FORBIDDEN = "FORBIDDEN"
    GAME_NOT_FOUND = "GAME_NOT_FOUND"
    ILLEGAL_MOVE = "ILLEGAL_MOVE"
    NOT_YOUR_TURN = "NOT_YOUR_TURN"
    STALE_BOARD = "STALE_BOARD"
    UNAUTHORIZED = "UNAUTHORIZED"

    def __str__(self) -> str:
        return str(self.value)
