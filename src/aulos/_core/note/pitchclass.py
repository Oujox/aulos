from __future__ import annotations

import typing as t
from typing import TYPE_CHECKING

from aulos._core.context import inject
from aulos._core.object import AulosObject
from aulos._core.pitch.schemas import PitchSchema
from aulos._core.utils import index

from .schemas import PitchClassSchema

if TYPE_CHECKING:
    from aulos._core.mode import Mode  # pragma: no cover
    from aulos._core.scale import Scale  # pragma: no cover


def resolve_pitchname_from_scale(pitchclass: int, scale: Scale | Mode | None, schema: PitchClassSchema) -> str | None:
    if scale is not None:
        relative_pitchclass = (pitchclass - int(scale.key)) % schema.classes
        if (idx := index(scale.positions, relative_pitchclass)) is not None:
            return schema.convert_pitchclass_to_pitchname(
                pitchclass,
                scale.signatures[idx],
            )
    return None


class BasePitchClass(AulosObject[PitchClassSchema]):
    """
    BasePitchClass represents a musical pitch class, which is
    a set of all pitches that are a whole number of octaves apart.

    This class provides the foundational structure for defining pitch classes, including properties and methods
    to handle pitch class numbers, pitch names, and their relationships within a scale.
    """

    _pitchclass: int
    _pitchnames: tuple[str | None, ...]
    _pitchname: str | None
    _scale: Scale | Mode | None

    @inject
    def __init__(
        self,
        identify: int | str | t.Self,
        *,
        scale: Scale | Mode | None = None,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)

        if isinstance(identify, BasePitchClass):
            pitchnames = self.schema.convert_pitchclass_to_pitchnames(identify.pitchclass)
            pitchname = resolve_pitchname_from_scale(identify.pitchclass, scale, self.schema)
            self._pitchclass = identify.pitchclass
            self._pitchnames = pitchnames
            self._pitchname = pitchname or identify.pitchname
            self._scale = scale or identify.scale

        elif self.is_pitchclass(identify):
            pitchnames = self.schema.convert_pitchclass_to_pitchnames(identify)
            pitchname = resolve_pitchname_from_scale(identify, scale, self.schema)
            self._pitchclass = identify
            self._pitchnames = pitchnames
            self._pitchname = pitchname
            self._scale = scale

        elif self.is_pitchname(identify):
            pitchclass = self.schema.convert_pitchname_to_picthclass(identify)
            pitchnames = self.schema.convert_pitchclass_to_pitchnames(pitchclass)
            pitchname = resolve_pitchname_from_scale(pitchclass, scale, self.schema)
            self._pitchclass = pitchclass
            self._pitchnames = pitchnames
            self._pitchname = pitchname or identify
            self._scale = scale

        else:
            raise ValueError

    def __init_subclass__(
        cls,
        *,
        intervals: t.Sequence[int],
        symbols_pitchclass: t.Sequence[str],
        symbols_accidental: t.Sequence[str],
    ) -> None:
        schema = PitchClassSchema(
            tuple(intervals),
            tuple(symbols_pitchclass),
            tuple(symbols_accidental),
            PitchSchema(),
        )
        super().__init_subclass__(schema=schema)

    @property
    def pitchclass(self) -> int:
        """Returns the pitch class as an integer."""
        return self._pitchclass

    @property
    def pitchnames(self) -> list[str]:
        """Returns the pitch names of the pitch class."""
        return [n for n in self._pitchnames if n is not None]

    @property
    def pitchname(self) -> str | None:
        """Returns the primary pitch name of the pitch class."""
        return self._pitchname

    @property
    def scale(self) -> Scale | Mode | None:
        """Returns the scale associated with the pitch class."""
        return self._scale

    @classmethod
    def is_pitchname(cls, pitchname: object) -> t.TypeGuard[str]:
        """Checks if the value is a valid pitch name."""
        return cls.schema.is_pitchname(pitchname)

    @classmethod
    def is_pitchclass(cls, pitchclass: object) -> t.TypeGuard[int]:
        """Checks if the value is a valid pitch class."""
        return cls.schema.is_pitchclass(pitchclass)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, t.SupportsInt):
            return NotImplemented
        return int(self) == int(other)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: t.SupportsInt) -> t.Self:
        pitchclass = (int(self) + int(other)) % self.schema.classes
        return self.__class__(pitchclass, scale=self.scale, setting=self.setting)

    def __sub__(self, other: t.SupportsInt) -> t.Self:
        pitchclass = (int(self) - int(other)) % self.schema.classes
        return self.__class__(pitchclass, scale=self.scale, setting=self.setting)

    def __int__(self) -> int:
        return self._pitchclass

    def __str__(self) -> str:
        return f"<PitchClass: {self.pitchname or self.pitchnames}, scale: {self.scale}>"

    def __repr__(self) -> str:
        return f"<PitchClass: {self.pitchname or self.pitchnames}, scale: {self.scale}>"
