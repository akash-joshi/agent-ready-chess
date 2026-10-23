from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="Move")



@_attrs_define
class Move:
    """ 
        Attributes:
            move (str): Move in SAN, for example "e4", "Nf3" or "O-O".
            board_version (int | None | Unset): Version you last read. If it is out of date, the move is rejected with
                STALE_BOARD.
     """

    move: str
    board_version: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        move = self.move

        board_version: int | None | Unset
        if isinstance(self.board_version, Unset):
            board_version = UNSET
        else:
            board_version = self.board_version


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "move": move,
        })
        if board_version is not UNSET:
            field_dict["board_version"] = board_version

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        move = d.pop("move")

        def _parse_board_version(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        board_version = _parse_board_version(d.pop("board_version", UNSET))


        move = cls(
            move=move,
            board_version=board_version,
        )


        move.additional_properties = d
        return move

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
