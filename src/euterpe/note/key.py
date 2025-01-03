import typing as t

from .._core import EuterpeObject
from ._base import BaseNote


class Key(BaseNote, EuterpeObject):

    _name: str
    _pitchclass: int
    _signatures: tuple[int, ...]

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(**kwargs)

        if self.is_keyname(name):
            self._name = name
            self._pitchclass = self.schema.convert_pitchname_to_picthclass(name)
            self._signatures = self.schema.generate_key_signatures(name)

        else:
            raise ValueError()

    @property
    def pitchname(self) -> str:
        return self._name

    @property
    def pitchclass(self) -> int:
        return self._pitchclass

    @property
    def signature(self) -> tuple[int, ...]:
        return self._signatures

    def is_keyname(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.schema.pitchnames

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, (int, BaseNote)):
            return NotImplemented
        return int(self) == int(other)

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __int__(self) -> int:
        return self._pitchclass

    def __str__(self) -> str:
        return f"<Key: {self._name}>"

    def __repr__(self) -> str:
        return f"Key(name={self._name!r}, setting={self._setting!r})"
