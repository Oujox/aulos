from __future__ import annotations

import typing as t

from .._core import AulosObject
from .pitchclass import BasePitchClass, PitchClassConvertible
from .schemas import KeySchema


class BaseKey[PITCHCLASS: BasePitchClass](AulosObject[KeySchema]):
    PitchClass: type[PITCHCLASS]
    _pitchname: str
    _pitchclass: int
    _signatures: tuple[int, ...]

    def __init__(self, identify: str | BaseKey, **kwargs) -> None:
        super().__init__(**kwargs)

        if isinstance(identify, BaseKey):
            self._pitchname = identify._pitchname
            self._pitchclass = identify._pitchclass
            self._signatures = identify._signatures

        elif self.is_keyname(identify):
            self._pitchname = identify
            self._pitchclass = self.schema.pitchclass.convert_pitchname_to_picthclass(
                identify
            )
            self._signatures = self.schema.generate_key_signatures(identify)

        else:
            raise ValueError()

    def __init_subclass__(
        cls, *, accidental: int, pitchclass: type[BasePitchClass], **kwargs
    ) -> None:
        schema = KeySchema(
            accidental,
            pitchclass.schema,
        )
        super().__init_subclass__(schema=schema, **kwargs)
        cls.PitchClass = pitchclass

    @property
    def keyname(self) -> str:
        return self._pitchname

    @property
    def signature(self) -> tuple[int, ...]:
        return self._signatures

    def to_pitchclass(self) -> PITCHCLASS:
        return self.PitchClass(self._pitchname, setting=self._setting)

    @classmethod
    def is_keyname(cls, value: t.Any) -> t.TypeGuard[str]:
        return cls.schema.is_keyname(value)

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, (int, PitchClassConvertible)):
            return NotImplemented
        return int(self) == int(other)

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __int__(self) -> int:
        return self._pitchclass

    def __str__(self) -> str:
        return f"<Key: {self.keyname}>"

    def __repr__(self) -> str:
        return f"<Key: {self.keyname}>"
