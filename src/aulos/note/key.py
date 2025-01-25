import typing as t

from .._core import AulosObject
from .pitchclass import BasePitchClass, _PitchClassLike
from .schemas import KeySchema


class BaseKey(AulosObject[KeySchema]):
    _pitchname: str
    _pitchclass: int
    _signatures: tuple[int, ...]

    def __init__(self, name: str, **kwargs) -> None:
        super().__init__(**kwargs)

        if self.is_keyname(name):
            self._pitchname = name
            self._pitchclass = self.schema.pitchclass.convert_pitchname_to_picthclass(
                name
            )
            self._signatures = self.schema.generate_key_signatures(name)

        else:
            raise ValueError()

    def __init_subclass__(
        cls, *, accidental: int, base: type[BasePitchClass], **kwargs
    ) -> None:
        schema = KeySchema(
            accidental,
            base.schema,
        )
        super().__init_subclass__(schema=schema, **kwargs)

    @property
    def name(self) -> str:
        return self._pitchname

    @property
    def pitchclass(self) -> int:
        return self._pitchclass

    @property
    def pitchname(self) -> str:
        return self._pitchname

    @property
    def pitchnames(self) -> list[str]:
        return [
            n
            for n in self.schema.pitchclass.convert_pitchclass_to_pitchnames(
                self._pitchclass
            )
            if n is not None
        ]

    @property
    def signature(self) -> tuple[int, ...]:
        return self._signatures

    @classmethod
    def is_keyname(cls, value: t.Any) -> t.TypeGuard[str]:
        return cls.schema.is_keyname(value)

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, (int, _PitchClassLike)):
            return NotImplemented
        return int(self) == int(other)

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __int__(self) -> int:
        return self._pitchclass

    def __str__(self) -> str:
        return f"<Key: {self.pitchname}>"

    def __repr__(self) -> str:
        return f"<Key: {self.pitchname}>"
