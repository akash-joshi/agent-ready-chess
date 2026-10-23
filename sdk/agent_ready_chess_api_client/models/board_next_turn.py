from enum import StrEnum

class BoardNextTurn(StrEnum):
    BLACK = "black"
    WHITE = "white"

    def __str__(self) -> str:
        return str(self.value)
