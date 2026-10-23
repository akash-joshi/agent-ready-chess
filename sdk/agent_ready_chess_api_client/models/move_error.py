from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.move_error_code import MoveErrorCode
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="MoveError")



@_attrs_define
class MoveError:
    """ 
        Attributes:
            code (MoveErrorCode): Stable, machine-readable error code. Branch on this, not on detail.
            detail (str): Human-readable explanation of why the request failed.
            hint (None | str | Unset): What to do next.
     """

    code: MoveErrorCode
    detail: str
    hint: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        code = self.code.value

        detail = self.detail

        hint: None | str | Unset
        if isinstance(self.hint, Unset):
            hint = UNSET
        else:
            hint = self.hint


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "code": code,
            "detail": detail,
        })
        if hint is not UNSET:
            field_dict["hint"] = hint

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        code = MoveErrorCode(d.pop("code"))




        detail = d.pop("detail")

        def _parse_hint(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        hint = _parse_hint(d.pop("hint", UNSET))


        move_error = cls(
            code=code,
            detail=detail,
            hint=hint,
        )


        move_error.additional_properties = d
        return move_error

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
