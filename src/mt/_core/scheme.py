from __future__ import annotations

import typing as t
from functools import cached_property
from typing import TYPE_CHECKING

from .bases.base import Base
from .coexistence import Coexistence
from .utils import diff

if TYPE_CHECKING:
    from .setting import Setting  # pragma: no cover


class Scheme(Coexistence, Base):

    def __init__(self, setting: Setting) -> None:
        self._setting = setting
        super().__init__(semitone=setting.pitchclass.semitone)

    def __eq__(self, other: t.Self) -> bool:
        return self._setting == other._setting

    def __ne__(self, other: t.Self) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return "<Scheme>"

    def __repr__(self) -> str:
        return "<Scheme>"

    @property
    def intervals(self) -> tuple[int]:
        return self._setting.pitchclass.intervals

    @property
    def positions(self) -> tuple[int]:
        return self._setting.pitchclass.positions

    @cached_property
    def pitchnames(self) -> tuple[str]:
        return tuple(self._setting.pitchclass.name2class.keys())

    @cached_property
    def pitchclasses(self) -> tuple[int]:
        return tuple(self._setting.pitchclass.class2name.keys())

    def generate_accidentals(self, pitchname: str) -> tuple[int]:
        if not self.is_pitchname(pitchname):
            raise ValueError(f"Invalid notename: '{pitchname}'.")

        positions = []
        r_symbol = self.convert_pitchname_to_symbol(pitchname)
        r_pitchclass = self.convert_pitchname_to_picthclass(pitchname)

        idx = self._setting.pitchclass.symbols.index(r_symbol)
        symbols = (
            self._setting.pitchclass.symbols[idx:]
            + self._setting.pitchclass.symbols[:idx]
        )

        for pos, symbol in zip(self._setting.pitchclass.positions, symbols):
            n_pos = self.convert_pitchname_to_picthclass(symbol)
            a_pos = (r_pitchclass + pos) % self.semitone
            positions.append(diff(a_pos, n_pos, self.semitone))
        return positions

    def count_accidental(self, pitchname: str) -> t.Optional[int]:
        if self.is_pitchname(pitchname):
            count_acc_upper = pitchname.count(
                self._setting.pitchclass.accidental.upper_symbol
            )
            count_acc_lower = pitchname.count(
                self._setting.pitchclass.accidental.lower_symbol
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
        return self.convert_pitchclass_to_pitchnames(pitchclass)[
            self._setting.pitchclass.accidental.limit + accidental
        ]

    def convert_pitchclass_to_pitchnames(
        self, pitchclass: int
    ) -> tuple[t.Optional[str]]:
        if not self.is_pitchclass(pitchclass):
            raise ValueError(f"Invalid pitchclass: '{pitchclass}'.")
        return self._setting.pitchclass.class2name[pitchclass]

    def convert_pitchname_to_picthclass(self, pitchname: str) -> int:
        if not self.is_pitchname(pitchname):
            raise ValueError(f"Invalid notename: '{pitchname}'.")
        return self._setting.pitchclass.name2class[pitchname]

    def convert_pitchname_to_symbol(self, pitchname: str):
        if not self.is_pitchname(pitchname):
            raise ValueError(f"Invalid notename: '{pitchname}'.")
        return pitchname.replace(
            self._setting.pitchclass.accidental.upper_symbol, ""
        ).replace(self._setting.pitchclass.accidental.lower_symbol, "")

    def is_symbol(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self._setting.pitchclass.symbols

    def is_pitchname(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.pitchnames

    def is_pitchclass(self, value: t.Any) -> t.TypeGuard[int]:
        return isinstance(value, int) and 0 <= value < self.semitone
