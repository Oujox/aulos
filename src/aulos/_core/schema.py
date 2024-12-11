from __future__ import annotations

import typing as t
from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .setting import Setting  # pragma: no cover


class Schema:

    def __init__(self, setting: Setting) -> None:
        self._setting = setting

    def __eq__(self, other: t.Self) -> bool:
        return self._setting == other._setting

    def __ne__(self, other: t.Self) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return "<Schema>"

    def __repr__(self) -> str:
        return "<Schema>"

    """
    PitchClass
    """

    @property
    def semitone(self) -> int:
        return self._setting.pitchclass.derive.semitone

    @property
    def intervals(self) -> tuple[int]:
        return self._setting.pitchclass.intervals

    @property
    def positions(self) -> tuple[int]:
        return self._setting.pitchclass.derive.positions

    @property
    def symbols(self) -> tuple[str]:
        return self._setting.pitchclass.symbols

    @cached_property
    def pitchnames(self) -> tuple[str]:
        return tuple(self._setting.pitchclass.derive.name2class.keys())

    @cached_property
    def pitchclasses(self) -> tuple[int]:
        return tuple(self._setting.pitchclass.derive.class2name.keys())

    def count_accidental(self, pitchname: str) -> t.Optional[int]:
        if self.is_pitchname(pitchname):
            count_acc_upper = pitchname.count(
                self._setting.pitchclass.accidental.symbol.sharp
            )
            count_acc_lower = pitchname.count(
                self._setting.pitchclass.accidental.symbol.flat
            )
            return count_acc_upper - count_acc_lower
        return None

    def convert_pitchclass_to_symbol(self, pitchclass: int) -> t.Optional[str]:
        if not self.is_pitchclass(pitchclass):
            raise ValueError(f"Invalid pitchclass: '{pitchclass}'.")
        return self.convert_pitchclass_to_pitchnames(pitchclass)[
            self._setting.pitchclass.accidental.limit
        ]

    def convert_pitchclass_to_pitchname(
        self, pitchclass: int, accidental: int
    ) -> t.Optional[str]:
        if not self.is_pitchclass(pitchclass):
            raise ValueError(f"Invalid pitchclass: '{pitchclass}'.")
        return self._setting.pitchclass.derive.class2name[pitchclass][
            self._setting.pitchclass.accidental.limit + accidental
        ]

    def convert_pitchclass_to_pitchnames(
        self, pitchclass: int
    ) -> tuple[t.Optional[str]]:
        if not self.is_pitchclass(pitchclass):
            raise ValueError(f"Invalid pitchclass: '{pitchclass}'.")
        return self._setting.pitchclass.derive.class2name[pitchclass]

    def convert_pitchname_to_picthclass(self, pitchname: str) -> int:
        if not self.is_pitchname(pitchname):
            raise ValueError(f"Invalid pitchname: '{pitchname}'.")
        return self._setting.pitchclass.derive.name2class[pitchname]

    def convert_pitchname_to_symbol(self, pitchname: str):
        if not self.is_pitchname(pitchname):
            raise ValueError(f"Invalid pitchname: '{pitchname}'.")
        return pitchname.replace(
            self._setting.pitchclass.accidental.symbol.sharp, ""
        ).replace(self._setting.pitchclass.accidental.symbol.flat, "")

    def is_symbol(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self._setting.pitchclass.symbols

    def is_pitchname(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.pitchnames

    def is_pitchclass(self, value: t.Any) -> t.TypeGuard[int]:
        return isinstance(value, int) and value in self.pitchclasses

    """
    Note
    """

    @cached_property
    def notenames(self) -> tuple[str]:
        return tuple(self._setting.note.derive.name2number.keys())

    @cached_property
    def notenumbers(self) -> tuple[int]:
        return tuple(self._setting.note.derive.number2name.keys())

    def convert_notenumber_to_notename(
        self, notenumber: int, accidental: int
    ) -> t.Optional[str]:
        if not self.is_notenumber(notenumber):
            raise ValueError(f"Invalid notenumber: '{notenumber}'.")
        return self._setting.note.derive.number2name[notenumber][
            self._setting.pitchclass.accidental.limit + accidental
        ]

    def convert_notenumber_to_notenames(
        self, notenumber: int
    ) -> tuple[t.Optional[str]]:
        if not self.is_notenumber(notenumber):
            raise ValueError(f"Invalid notenumber: '{notenumber}'.")
        return self._setting.note.derive.number2name[notenumber]

    def convert_notename_to_notenumber(self, notename: str) -> int:
        if not self.is_notename(notename):
            raise ValueError(f"Invalid notename: '{notename}'.")
        return self._setting.note.derive.name2number[notename]

    def is_notename(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.notenames

    def is_notenumber(self, value: t.Any) -> t.TypeGuard[int]:
        return isinstance(value, int) and value in self.notenumbers

    """
    Extension
    """

    def convert_notenumber_to_pitchclass(self, notenumber: int) -> int:
        if not self.is_notenumber(notenumber):
            raise ValueError(f"Invalid notenumber: '{notenumber}'.")
        return notenumber % self.semitone

    def convert_pitchclass_to_notenumber(self, pitchclass: int, octnumber: int) -> int:
        if not self.is_pitchclass(pitchclass):
            raise ValueError(f"Invalid pitchclass: '{pitchclass}'.")
        return pitchclass + (self.semitone * octnumber)

    def convert_notename_to_pitchname(self, notename: str) -> str:
        if not self.is_notename(notename):
            raise ValueError(f"Invalid notename: '{notename}'.")
        notenumber = self.convert_notename_to_notenumber(notename)
        for pitchname in self.convert_notenumber_to_notenames(notenumber):
            if pitchname is not None and notename.find(pitchname) > 0:
                return pitchname
        raise ValueError("Not Reachable.")

    def convert_pitchname_to_notename(self, pitchname: str, octnumber: int) -> str:
        if not self.is_pitchname(pitchname):
            raise ValueError(f"Invalid pitchname: '{pitchname}'.")
        notesymbol = self._setting.note.presentation.symbols[octnumber]
        return create_notename_from_notesymbol(pitchname, notesymbol)


def create_notename_from_notesymbol(pitchname: str, symbol: str):
    # <N>
    if symbol.find("<N>") >= 0:
        return symbol.replace("<N>", pitchname, 1)
    # <n>
    elif symbol.find("<n>") >= 0:
        return symbol.replace("<n>", pitchname, 1)
    # Not Reachable
    raise ValueError()
