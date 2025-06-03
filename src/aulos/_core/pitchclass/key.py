import typing as t
from typing import cast

from aulos._core.context import inject
from aulos._core.object import AulosObject
from aulos._core.utils import classproperty

from .pitchclass import BasePitchClass
from .schemas import KeySchema


class BaseKey[PITCHCLASS: BasePitchClass](AulosObject[KeySchema]):
    """
    BaseKey class represents a musical key in a theoretical context.

    This class provides the foundational structure for defining and manipulating musical keys.
    It includes properties and methods to handle key names, key classes, and key signatures.
    """

    _PitchClass: t.ClassVar[type[BasePitchClass]]

    _keyname: str
    _pitchclass: int
    _signatures: tuple[int, ...]

    @inject
    def __init__(self, identify: str | t.Self, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)

        if isinstance(identify, BaseKey):
            self._keyname = identify.keyname
            self._pitchclass = self.schema.pitchclass.convert_pitchname_to_picthclass(identify.keyname)
            self._signatures = self.schema.generate_key_signatures(identify.keyname)

        elif self.is_keyname(identify):
            self._keyname = identify
            self._pitchclass = self.schema.pitchclass.convert_pitchname_to_picthclass(identify)
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
        cls._PitchClass = pitchclass

    @classproperty
    def PitchClass(self) -> type[PITCHCLASS]:  # noqa: N802
        """The type of pitch class associated with the key."""
        return cast("type[PITCHCLASS]", self._PitchClass)

    @property
    def keyname(self) -> str:
        """Returns the name of the key."""
        return self._keyname

    @property
    def signature(self) -> tuple[int, ...]:
        """Returns the signature of the key."""
        return self._signatures

    def to_pitchclass(self) -> PITCHCLASS:
        """Returns the pitch class of the key."""
        return self.PitchClass(self._keyname, setting=self._setting)

    @classmethod
    def is_keyname(cls, value: object) -> t.TypeGuard[str]:
        """Checks if the value is a valid key name."""
        return cls.schema.is_keyname(value)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, t.SupportsInt):
            return NotImplemented
        return int(self) == int(other)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __int__(self) -> int:
        return self._pitchclass

    def __str__(self) -> str:
        return f"<Key: {self.keyname}>"

    def __repr__(self) -> str:
        return f"<Key: {self.keyname}>"
