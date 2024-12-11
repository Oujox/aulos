from __future__ import annotations

import typing as t
from functools import cached_property

from .._core import AulosObject
from .._core.framework import inject
from .._core.utils import diff
from ._base import BaseNote


class Key(BaseNote, AulosObject):

    @inject
    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(**kwargs)

        if self.is_keyname(name):
            self._name = name
            self._pitchclass = self.schema.convert_pitchname_to_picthclass(name)

        else:
            raise ValueError()

    @property
    def pitchname(self) -> str:
        return self._name

    @property
    def pitchclass(self) -> int:
        return self._pitchclass

    @cached_property
    def accsidentals(self) -> tuple[int]:
        positions = []
        r_symbol = self.schema.convert_pitchname_to_symbol(self.pitchname)
        r_pitchclass = self.schema.convert_pitchname_to_picthclass(self.pitchname)

        idx = self.schema.symbols.index(r_symbol)
        symbols = self.schema.symbols[idx:] + self.schema.symbols[:idx]

        for pos, symbol in zip(self.schema.positions, symbols):
            n_pos = self.schema.convert_pitchname_to_picthclass(symbol)
            a_pos = (r_pitchclass + pos) % self.schema.semitone
            positions.append(diff(a_pos, n_pos, self.schema.semitone))
        return positions

    def __eq__(self, other: int | BaseNote) -> bool:
        return self._pitchclass == int(other)

    def __ne__(self, other: int | BaseNote) -> bool:
        return not self.__eq__(other)

    def __int__(self) -> int:
        return self._pitchclass

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return "<Key: {}>".format(self._name)

    def is_keyname(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.schema.pitchnames
