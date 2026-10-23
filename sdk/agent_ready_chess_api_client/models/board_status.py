from enum import StrEnum

class BoardStatus(StrEnum):
    CHECKMATE = "checkmate"
    DRAW = "draw"
    IN_PROGRESS = "in_progress"
    STALEMATE = "stalemate"

    def __str__(self) -> str:
        return str(self.value)
