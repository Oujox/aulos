import typing as t
from typing import TYPE_CHECKING

from .._core import AulosObject
from .._core.utils import index
from .pitchclass import BasePitchClass
from .schemas import NoteSchema

if TYPE_CHECKING:
    from ..scale import Scale  # pragma: no cover
    from ..tuner import Tuner  # pragma: no cover


class BaseNote[PITCHCLASS: BasePitchClass](AulosObject[NoteSchema]):
    PitchClass: type[PITCHCLASS]
    _notenumber: int
    _notenames: tuple[str | None, ...]
    _notename: str | None
    _tuner: t.Optional["Tuner"]
    _scale: t.Optional["Scale"]

    def __init__(
        self,
        identify: int | str,
        *,
        tuner: t.Optional["Tuner"] = None,
        scale: t.Optional["Scale"] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        if isinstance(identify, BaseNote):
            self._notenumber = identify._notenumber
            self._notenames = identify._notenames
            self._notename = identify._notename
            self._scale = None
            self._tuner = identify._tuner
            self.scale = identify._scale

        elif self.is_notenumber(identify):
            notenames = self.schema.convert_notenumber_to_notenames(identify)
            self._notenumber = identify
            self._notenames = notenames
            self._notename = None
            self._scale = None
            self._tuner = tuner
            self.scale = scale

        elif self.is_notename(identify):
            notenumber = self.schema.convert_notename_to_notenumber(identify)
            notenames = self.schema.convert_notenumber_to_notenames(notenumber)
            self._notenumber = notenumber
            self._notenames = notenames
            self._notename = identify
            self._scale = None
            self._tuner = tuner
            self.scale = scale

        else:
            raise ValueError()

    def __init_subclass__(
        cls,
        *,
        symbols_notenumber: t.Sequence[int],
        symbols_octave: t.Sequence[str],
        reference_notenumber: int,
        reference_octave: int,
        pitchclass: type[PITCHCLASS],
        **kwargs,
    ) -> None:
        schema = NoteSchema(
            tuple(symbols_notenumber),
            tuple(symbols_octave),
            reference_notenumber,
            reference_octave,
            pitchclass.schema,
        )
        super().__init_subclass__(schema=schema, **kwargs)
        cls.PitchClass = pitchclass

    @property
    def notenumber(self) -> int:
        return self._notenumber

    @property
    def notenames(self) -> list[str]:
        return [n for n in self._notenames if n is not None]

    @property
    def notename(self) -> str | None:
        return self._notename

    @notename.setter
    def notename(self, name: str):
        if self.is_notename(name) and name in self._notenames:
            self._notename = name

    @property
    def tuner(self) -> t.Optional["Tuner"]:
        return self._tuner

    @tuner.setter
    def tuner(self, tuner: t.Optional["Tuner"]):
        from ..tuner import Tuner

        if isinstance(tuner, Tuner):
            self._tuner = tuner

    @property
    def scale(self) -> t.Optional["Scale"]:
        return self._scale

    @scale.setter
    def scale(self, scale: t.Optional["Scale"]):
        from ..scale import Scale

        if isinstance(scale, Scale):
            self._scale = scale
            pitchclass = self.schema.convert_notenumber_to_pitchclass(self._notenumber)
            pitchclass = (
                pitchclass - scale.key.pitchclass
            ) % self.schema.pitchclass.cardinality

            if (idx := index(scale.positions, pitchclass)) is not None:
                self._notename = self.schema.convert_notenumber_to_notename(
                    self._notenumber, scale.signatures[idx]
                )

    @property
    def hz(self) -> float | None:
        if self._tuner is None:
            return None
        return self._tuner.hz(self._notenumber)

    def to_pitchclass(self) -> PITCHCLASS:
        pitchlass = self.schema.convert_notenumber_to_pitchclass(self._notenumber)
        return self.PitchClass(
            pitchlass, tuner=self._tuner, scale=self._scale, setting=self._setting
        )

    @classmethod
    def is_notename(cls, notename: t.Any) -> t.TypeGuard[str]:
        return cls.schema.is_notename(notename)

    @classmethod
    def is_notenumber(cls, notenumber: t.Any) -> t.TypeGuard[int]:
        return cls.schema.is_notenumber(notenumber)

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, t.SupportsInt):
            return NotImplemented
        return int(self) == int(other)

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: t.SupportsInt) -> t.Self:
        return self.__class__(
            int(self) + int(other), scale=self.scale, setting=self.setting
        )

    def __sub__(self, other: t.SupportsInt) -> t.Self:
        return self.__class__(
            int(self) - int(other), scale=self.scale, setting=self.setting
        )

    def __int__(self):
        return self._notenumber

    def __str__(self) -> str:
        return f"<Note: {self.notename or self.notenames}, scale: {self.scale}>"

    def __repr__(self) -> str:
        return f"<Note: {self.notename or self.notenames}, scale: {self.scale}>"
