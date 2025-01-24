from __future__ import annotations

import typing as t
from typing import TYPE_CHECKING

from .._core import AulosObject
from .._core.utils import index
from .pitchclass import BasePitchClass, _PitchClassLike
from .schemas import NoteSchema

if TYPE_CHECKING:
    from ..scale import BaseScale  # pragma: no cover
    from ..tuner import BaseTuner  # pragma: no cover


class BaseNote(AulosObject[NoteSchema]):

    _notenumber: int
    _notenames: tuple[str | None, ...]
    _notename: str | None
    _tuner: BaseTuner | None
    _scale: BaseScale | None

    def __init__(
        self,
        identify: int | str,
        *,
        scale: BaseScale | None = None,
        tuner: BaseTuner | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        if self.is_notenumber(identify):
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
        base: type[BasePitchClass],
        **kwargs,
    ) -> None:
        schema = NoteSchema(
            tuple(symbols_notenumber),
            tuple(symbols_octave),
            reference_notenumber,
            reference_octave,
            base.schema,
        )
        super().__init_subclass__(schema=schema, **kwargs)

    @property
    def notenumber(self) -> int:
        return self._notenumber

    @property
    def notename(self) -> str | None:
        return self._notename

    @property
    def notenames(self) -> list[str]:
        return [n for n in self._notenames if n is not None]

    @property
    def pitchclass(self) -> int:
        return self.schema.convert_notenumber_to_pitchclass(self._notenumber)

    @property
    def pitchname(self) -> str | None:
        if self._notename is None:
            return None
        return self.schema.convert_notename_to_pitchname(self._notename)

    @property
    def pitchnames(self) -> list[str]:
        return [
            n
            for n in self.schema.pitchclass.convert_pitchclass_to_pitchnames(
                self.pitchclass
            )
            if n is not None
        ]

    @notename.setter
    def notename(self, name: str):
        if self.is_notename(name) and name in self._notenames:
            self._notename = name

    @property
    def tuner(self) -> BaseTuner | None:
        return self._tuner

    @property
    def scale(self) -> BaseScale | None:
        return self._scale

    @tuner.setter
    def tuner(self, tuner: BaseTuner):
        from ..tuner import BaseTuner

        if isinstance(tuner, BaseTuner):
            self._tuner = tuner

    @scale.setter
    def scale(self, scale: BaseScale | None):
        from ..scale import BaseScale

        if isinstance(scale, BaseScale):
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

    @classmethod
    def is_notename(cls, notename: t.Any) -> t.TypeGuard[str]:
        return cls.schema.is_notename(notename)

    @classmethod
    def is_notenumber(cls, notenumber: t.Any) -> t.TypeGuard[int]:
        return cls.schema.is_notenumber(notenumber)

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, (int, _PitchClassLike)):
            return NotImplemented
        return int(self) == int(other)

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: int | _PitchClassLike) -> t.Self:
        return self.__class__(
            int(self) + int(other), scale=self.scale, setting=self.setting
        )

    def __sub__(self, other: int | _PitchClassLike) -> t.Self:
        return self.__class__(
            int(self) - int(other), scale=self.scale, setting=self.setting
        )

    def __int__(self):
        return self._notenumber

    def __str__(self) -> str:
        return f"<Note: {self.notename or self.notenames}, scale: {self.scale}>"

    def __repr__(self) -> str:
        return f"<Note: {self.notename or self.notenames}, scale: {self.scale}>"
