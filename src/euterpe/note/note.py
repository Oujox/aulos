from __future__ import annotations

import typing as t
from typing import TYPE_CHECKING

from .._core import EuterpeObject
from .._core.utils import index
from ._base import BaseNote

if TYPE_CHECKING:
    from ..scale import Scale


class Note(BaseNote, EuterpeObject):

    _notenumber: int
    _notenames: tuple[str | None]
    _notename: str | None
    _scale: Scale | None

    def __init__(
        self, identify: int | str, *, scale: Scale | None = None, **kwargs
    ) -> None:
        super().__init__(**kwargs)

        if self.schema.is_notenumber(identify):
            notenames = self.schema.convert_notenumber_to_notenames(identify)
            self._notenumber = identify
            self._notenames = notenames
            self._notename = None
            self._scale = None
            self.scale = scale

        elif self.schema.is_notename(identify):
            notenumber = self.schema.convert_notename_to_notenumber(identify)
            notenames = self.schema.convert_notenumber_to_notenames(notenumber)
            self._notenumber = notenumber
            self._notenames = notenames
            self._notename = identify
            self._scale = None
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
    def scale(self) -> Scale | None:
        return self._scale

    @notename.setter
    def notename(self, name: str):
        if self.is_notename(name) and name in self._notenames:
            self._notename = name

    @scale.setter
    def scale(self, scale: Scale):
        from ..scale import Scale

        if isinstance(scale, Scale):
            pitchclass = self.schema.convert_notenumber_to_pitchclass(self._notenumber)
            pitchclass = (pitchclass - scale.key.pitchclass) % self.schema.semitone
            if (idx := index(scale.positions, pitchclass)) is None:
                return
            acc, kacc = scale.accidentals[idx], scale.key.accsidentals[idx]
            self._notename = self.schema.convert_notenumber_to_notename(
                self._notenumber, acc + kacc
            )
            self._scale = scale

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, (int, BaseNote)):
            return NotImplemented
        return int(self) == int(other)

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: int | BaseNote) -> Note:
        return Note(int(self) + int(other), scale=self.scale, setting=self.setting)

    def __sub__(self, other: int | BaseNote) -> Note:
        return Note(int(self) - int(other), scale=self.scale, setting=self.setting)

    def __int__(self):
        return self._notenumber

    def __str__(self) -> str:
        return self._notename or str(self._notenumber)

    def __repr__(self) -> str:
        return "<Note: {}>".format(self._notename or str(self.notenames))

    def is_notename(self, notename: t.Any) -> t.TypeGuard[str]:
        return self.schema.is_notename(notename)

    def is_notenumber(self, notenumber: t.Any) -> t.TypeGuard[int]:
        return self.schema.is_notenumber(notenumber)
