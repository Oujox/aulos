from __future__ import annotations

import typing as t
from typing import TYPE_CHECKING

from .._core import EuterpeObject
from .._core.utils import index
from ._base import BaseNote

# type annotaion
if TYPE_CHECKING:
    from scale import Scale  # pragma: no cover


class PitchClass(BaseNote, EuterpeObject):

    _pitchclass: int
    _pitchnames: tuple[str | None, ...]
    _pitchname: str | None
    _scale: Scale | None

    def __init__(
        self, identify: int | str, *, scale: Scale | None = None, **kwargs
    ) -> None:
        super().__init__(**kwargs)

        if self.is_pitchclass(identify):
            pitchnames = self.schema.convert_pitchclass_to_pitchnames(identify)
            self._pitchclass = identify
            self._pitchnames = pitchnames
            self._pitchname = None
            self._scale = None
            self.scale = scale

        elif self.is_pitchname(identify):
            pitchclass = self.schema.convert_pitchname_to_picthclass(identify)
            pitchnames = self.schema.convert_pitchclass_to_pitchnames(pitchclass)
            self._pitchclass = pitchclass
            self._pitchnames = pitchnames
            self._pitchname = identify
            self._scale = None
            self.scale = scale

        else:
            raise ValueError()

    @property
    def pitchclass(self) -> int:
        return self._pitchclass

    @property
    def pitchname(self) -> str | None:
        return self._pitchname

    @property
    def pitchnames(self) -> list[str]:
        return [n for n in self._pitchnames if n is not None]

    @property
    def scale(self) -> Scale | None:
        return self._scale

    @pitchname.setter
    def pitchname(self, name: str):
        if self.is_pitchname(name) and name in self._pitchnames:
            self._pitchname = name

    @scale.setter
    def scale(self, scale: Scale | None):
        from ..scale import Scale

        if isinstance(scale, Scale):
            self._scale = scale
            pitchclass = (self.pitchclass - scale.key.pitchclass) % self.schema.semitone
    
            if (idx := index(scale._positions, pitchclass)) is not None:
                acc, kacc = scale._accidentals[idx], scale.key.accsidentals[idx]
                self._pitchname = self.schema.convert_pitchclass_to_pitchname(
                    self._pitchclass, acc + kacc
                )

            elif (idx := index(scale.positions, pitchclass)) is not None:
                dacc = scale.accidentals[idx]
                pitchclass = (pitchclass - dacc) % self.schema.semitone
                if (idx := index(scale._positions, pitchclass)) is not None:
                    acc, kacc = scale._accidentals[idx], scale.key.accsidentals[idx]
                    self._pitchname = self.schema.convert_pitchclass_to_pitchname(
                        self._pitchclass, acc + kacc + dacc
                    )

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, (int, BaseNote)):
            return NotImplemented
        return int(self) == int(other)

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: int | BaseNote) -> PitchClass:
        pitchclass = (int(self) + int(other)) % self.schema.semitone
        return PitchClass(pitchclass, scale=self.scale, setting=self.setting)

    def __sub__(self, other: int | BaseNote) -> PitchClass:
        pitchclass = (int(self) - int(other)) % self.schema.semitone
        return PitchClass(pitchclass, scale=self.scale, setting=self.setting)

    def __int__(self) -> int:
        return self._pitchclass

    def __str__(self) -> str:
        return self._pitchname or str(self._pitchclass)

    def __repr__(self) -> str:
        return "<PitchClass: {}>".format(self.pitchname or str(self.pitchnames))

    def is_pitchname(self, pitchname: t.Any) -> t.TypeGuard[str]:
        return self.schema.is_pitchname(pitchname)

    def is_pitchclass(self, pitchclass: t.Any) -> t.TypeGuard[int]:
        return self.schema.is_pitchclass(pitchclass)
