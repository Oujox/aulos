from __future__ import annotations

import typing as t
from typing import TYPE_CHECKING, cast

from aulos._core.context import inject
from aulos._core.object import AulosObject
from aulos._core.pitchclass import BasePitchClass
from aulos._core.utils import classproperty, index

from .schemas import NoteSchema

if TYPE_CHECKING:
    from aulos._core.mode import Mode  # pragma: no cover
    from aulos._core.scale import Scale  # pragma: no cover
    from aulos._core.tuner import Tuner  # pragma: no cover


def resolve_notename_from_scale(notenumber: int, scale: Scale | Mode | None, schema: NoteSchema) -> str | None:
    if scale is not None:
        relative_pitchclass = schema.convert_notenumber_to_pitchclass(notenumber)
        relative_pitchclass = (relative_pitchclass - int(scale.key)) % schema.pitchclass.classes
        if (idx := index(scale.positions, relative_pitchclass)) is not None:
            return schema.convert_notenumber_to_notename(
                notenumber,
                scale.signatures[idx],
            )
    return None


class BaseNote[PITCHCLASS: BasePitchClass](AulosObject[NoteSchema]):
    """
    BaseNote class represents a musical note with various properties and methods for manipulation.

    This class provides the foundational structure for defining musical notes, including properties and methods
    to handle note numbers, note names, and their relationships with pitch classes and scales.
    """

    _PitchClass: t.ClassVar[type[BasePitchClass]]

    _notenumber: int
    _notenames: tuple[str | None, ...]
    _notename: str | None
    _tuner: Tuner | None
    _scale: Scale | Mode | None

    @inject
    def __init__(
        self,
        identify: int | str | t.Self,
        *,
        tuner: Tuner | None = None,
        scale: Scale | Mode | None = None,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)

        if isinstance(identify, BaseNote):
            notenames = self.schema.convert_notenumber_to_notenames(identify.notenumber)
            notename = resolve_notename_from_scale(identify.notenumber, scale, self.schema)
            self._notenumber = identify.notenumber
            self._notenames = notenames
            self._notename = notename or identify.notename
            self._tuner = tuner or identify.tuner
            self._scale = scale or identify.scale

        elif self.is_notenumber(identify):
            notenames = self.schema.convert_notenumber_to_notenames(identify)
            notename = resolve_notename_from_scale(identify, scale, self.schema)
            self._notenumber = identify
            self._notenames = notenames
            self._notename = notename
            self._tuner = tuner
            self._scale = scale

        elif self.is_notename(identify):
            notenumber = self.schema.convert_notename_to_notenumber(identify)
            notenames = self.schema.convert_notenumber_to_notenames(notenumber)
            notename = resolve_notename_from_scale(notenumber, scale, self.schema)
            self._notenumber = notenumber
            self._notenames = notenames
            self._notename = notename or identify
            self._tuner = tuner
            self._scale = scale

        else:
            raise ValueError

    def __init_subclass__(
        cls,
        *,
        symbols_notenumber: t.Sequence[int],
        symbols_octave: t.Sequence[str],
        pitchclass: type[PITCHCLASS],
    ) -> None:
        schema = NoteSchema(
            tuple(symbols_notenumber),
            tuple(symbols_octave),
            pitchclass.schema,
        )
        super().__init_subclass__(schema=schema)
        cls._PitchClass = pitchclass

    @classproperty
    def PitchClass(self) -> type[PITCHCLASS]:  # noqa: N802
        """The type of pitch class associated with the note."""
        return cast("type[PITCHCLASS]", self._PitchClass)

    @property
    def notenumber(self) -> int:
        """Returns the note number of the note."""
        return self._notenumber

    @property
    def notenames(self) -> list[str]:
        """Returns the note names of the note."""
        return [n for n in self._notenames if n is not None]

    @property
    def notename(self) -> str | None:
        """Returns the note name of the note."""
        return self._notename

    @property
    def tuner(self) -> Tuner | None:
        """Returns the tuner of the note."""
        return self._tuner

    @property
    def scale(self) -> Scale | Mode | None:
        """Returns the scale of the note."""
        return self._scale

    @property
    def hz(self) -> float | None:
        """Returns the frequency of the note in hertz."""
        if self._tuner is None:
            return None
        return self._tuner.hz(self._notenumber)

    def to_pitchclass(self) -> PITCHCLASS:
        """Returns the pitch class of the note."""
        identify = (
            self.schema.convert_notename_to_pitchname(self._notename)
            if self._notename is not None
            else self.schema.convert_notenumber_to_pitchclass(self._notenumber)
        )
        return self.PitchClass(
            identify,
            scale=self._scale,
            setting=self._setting,
        )

    @classmethod
    def is_notename(cls, notename: object) -> t.TypeGuard[str]:
        """Checks if the value is a valid note name."""
        return cls.schema.is_notename(notename)

    @classmethod
    def is_notenumber(cls, notenumber: object) -> t.TypeGuard[int]:
        """Checks if the value is a valid note number."""
        return cls.schema.is_notenumber(notenumber)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, t.SupportsInt):
            return NotImplemented
        return int(self) == int(other)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: t.SupportsInt) -> t.Self:
        return self.__class__(
            int(self) + int(other),
            scale=self._scale,
            tuner=self._tuner,
            setting=self._setting,
        )

    def __sub__(self, other: t.SupportsInt) -> t.Self:
        return self.__class__(
            int(self) - int(other),
            scale=self._scale,
            tuner=self._tuner,
            setting=self._setting,
        )

    def __int__(self) -> int:
        return self._notenumber

    def __str__(self) -> str:
        return f"<Note: {self.notename or self.notenames}, scale: {self.scale}>"

    def __repr__(self) -> str:
        return f"<Note: {self.notename or self.notenames}, scale: {self.scale}>"
