import typing as t

from aulos._core import AulosObject

from .pitchclass import BasePitchClass
from .schemas import KeySchema


class BaseKey[PITCHCLASS: BasePitchClass](AulosObject[KeySchema]):
    """
    BaseKey class represents a musical key and provides methods to handle key-related operations.

    Attributes:
        PitchClass (type[PITCHCLASS]): The pitch class type associated with the key.
        _keyname (str): The name of the key.
        _keyclass (int): The class of the key.
        _signatures (tuple[int, ...]): The key signatures.
    """

    PitchClass: type[PITCHCLASS]
    _keyname: str
    _keyclass: int
    _signatures: tuple[int, ...]

    __slots__ = "_keyclass", "_keyname", "_signature"

    def __init__(self, identify: str | t.Self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)

        if isinstance(identify, BaseKey):
            self._keyname = identify.keyname
            self._keyclass = self.schema.pitchclass.convert_pitchname_to_picthclass(identify.keyname)
            self._signatures = self.schema.generate_key_signatures(identify.keyname)

        elif self.is_keyname(identify):
            self._keyname = identify
            self._keyclass = self.schema.pitchclass.convert_pitchname_to_picthclass(identify)
            self._signatures = self.schema.generate_key_signatures(identify)

        else:
            raise ValueError

    def __init_subclass__(
        cls,
        *,
        accidental: int,
        pitchclass: type[BasePitchClass],
    ) -> None:
        schema = KeySchema(
            accidental,
            pitchclass.schema,
        )
        super().__init_subclass__(schema=schema)
        cls.PitchClass = pitchclass

    @property
    def keyname(self) -> str:
        return self._keyname

    @property
    def signature(self) -> tuple[int, ...]:
        return self._signatures

    def to_pitchclass(self) -> PITCHCLASS:
        return self.PitchClass(self._keyname, setting=self._setting)

    @classmethod
    def is_keyname(cls, value: object) -> t.TypeGuard[str]:
        return cls.schema.is_keyname(value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, t.SupportsInt):
            return NotImplemented
        return int(self) == int(other)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __int__(self) -> int:
        return self._keyclass

    def __str__(self) -> str:
        return f"<Key: {self.keyname}>"

    def __repr__(self) -> str:
        return f"<Key: {self.keyname}>"
