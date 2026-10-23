from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.board_next_turn import BoardNextTurn
from ..models.board_status import BoardStatus
from typing import cast






T = TypeVar("T", bound="Board")



@_attrs_define
class Board:
    """ 
        Attributes:
            id (str):
            fen (str): Board position in FEN.
            board_version (int):
            next_turn (BoardNextTurn):
            status (BoardStatus):
            legal_moves (list[str]): Legal moves for the side to move, in SAN.
     """

    id: str
    fen: str
    board_version: int
    next_turn: BoardNextTurn
    status: BoardStatus
    legal_moves: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        fen = self.fen

        board_version = self.board_version

        next_turn = self.next_turn.value

        status = self.status.value

        legal_moves = self.legal_moves




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "fen": fen,
            "board_version": board_version,
            "next_turn": next_turn,
            "status": status,
            "legal_moves": legal_moves,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        fen = d.pop("fen")

        board_version = d.pop("board_version")

        next_turn = BoardNextTurn(d.pop("next_turn"))




        status = BoardStatus(d.pop("status"))




        legal_moves = cast(list[str], d.pop("legal_moves"))


        board = cls(
            id=id,
            fen=fen,
            board_version=board_version,
            next_turn=next_turn,
            status=status,
            legal_moves=legal_moves,
        )


        board.additional_properties = d
        return board

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
