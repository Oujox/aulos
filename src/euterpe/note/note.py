from __future__ import annotations

import typing as t
from typing import TYPE_CHECKING

from .._core import EuterpeObject
from .._core.utils import index
from ._base import BasePitchClass

if TYPE_CHECKING:
    from ..scale import Scale  # pragma: no cover
    from ..tuner import Tuner  # pragma: no cover


class Note(BasePitchClass, EuterpeObject):

    _notenumber: int
    _notenames: tuple[str | None, ...]
    _notename: str | None
    _tuner: Tuner | None
    _scale: Scale | None

    def __init__(
        self,
        identify: int | str,
        *,
        scale: Scale | None = None,
        tuner: Tuner | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        if self.schema.is_notenumber(identify):
            notenames = self.schema.convert_notenumber_to_notenames(identify)
            self._notenumber = identify
            self._notenames = notenames
            self._notename = None
            self._scale = None
            self._tuner = tuner
            self.scale = scale

        elif self.schema.is_notename(identify):
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
            for n in self.schema.convert_pitchclass_to_pitchnames(self.pitchclass)
            if n is not None
        ]

    @notename.setter
    def notename(self, name: str):
        if self.is_notename(name) and name in self._notenames:
            self._notename = name

    @property
    def tuner(self) -> Tuner | None:
        return self._tuner

    @property
    def scale(self) -> Scale | None:
        return self._scale

    @tuner.setter
    def tuner(self, tuner: Tuner):
        from ..tuner import Tuner

        if isinstance(tuner, Tuner):
            self._tuner = tuner

    @scale.setter
    def scale(self, scale: Scale | None):
        from ..scale import Scale

        if isinstance(scale, Scale):
            self._scale = scale
            pitchclass = self.schema.convert_notenumber_to_pitchclass(self._notenumber)
            pitchclass = (pitchclass - scale.key.pitchclass) % self.schema.semitone

            if (idx := index(scale.positions, pitchclass)) is not None:
                self._notename = self.schema.convert_notenumber_to_notename(
                    self._notenumber, scale.signatures[idx]
                )

    @property
    def hz(self) -> float | None:
        if self._tuner is None:
            return None
        return self._tuner.hz(self._notenumber)

    def is_notename(self, notename: t.Any) -> t.TypeGuard[str]:
        return self.schema.is_notename(notename)

    def is_notenumber(self, notenumber: t.Any) -> t.TypeGuard[int]:
        return self.schema.is_notenumber(notenumber)

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, (int, BasePitchClass)):
            return NotImplemented
        return int(self) == int(other)

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: int | BasePitchClass) -> Note:
        return Note(int(self) + int(other), scale=self.scale, setting=self.setting)

    def __sub__(self, other: int | BasePitchClass) -> Note:
        return Note(int(self) - int(other), scale=self.scale, setting=self.setting)

    def __int__(self):
        return self._notenumber

    def __str__(self) -> str:
        return f"<Note: {self.notename or self.notenames}, scale: {self.scale}>"

    def __repr__(self) -> str:
        return f"<Note: {self.notename or self.notenames}, scale: {self.scale}>"
