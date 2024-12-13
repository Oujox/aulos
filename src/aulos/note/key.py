import typing as t

from .._core import AulosObject
from ._base import BaseNote


class Key(BaseNote, AulosObject):

    _name: str
    _pitchclass: int
    _accidentals: tuple[int]

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(**kwargs)

        if self.is_keyname(name):
            self._name = name
            self._pitchclass = self.schema.convert_pitchname_to_picthclass(name)
            self._accidentals = self.schema.generate_key_accidentals(name)

        else:
            raise ValueError()

    @property
    def pitchname(self) -> str:
        return self._name

    @property
    def pitchclass(self) -> int:
        return self._pitchclass

    @property
    def accsidentals(self) -> tuple[int]:
        return self._accidentals

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
