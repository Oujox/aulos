from __future__ import annotations

import typing as t
from functools import cached_property

from .._core import Object
from .._core.context import inject
from ._base import BaseNote


class Key(BaseNote, Object):

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
        return self.schema.generate_accidentals(self._name)

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
