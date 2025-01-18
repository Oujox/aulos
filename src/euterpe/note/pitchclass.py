from __future__ import annotations

import typing as t
from typing import TYPE_CHECKING

from .._core import EuterpeObject
from .._core.utils import index
from .schemas import PitchClassSchema

# type annotaion
if TYPE_CHECKING:
    from ..scale import _Scale  # pragma: no cover


@t.runtime_checkable
class _PitchClassLike(t.Protocol):
    def __int__(self) -> int: ...

    @property
    def pitchclass(self) -> int: ...

    @property
    def pitchname(self) -> str | None: ...

    @property
    def pitchnames(self) -> list[str]: ...


class _PitchClass(EuterpeObject[PitchClassSchema]):

    _pitchclass: int
    _pitchnames: tuple[str | None, ...]
    _pitchname: str | None
    _scale: _Scale | None

    def __init__(
        self, identify: int | str, *, scale: _Scale | None = None, **kwargs
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

    def __init_subclass__(
        cls,
        *,
        intervals: t.Sequence[int],
        symbols_pitchclass: t.Sequence[str],
        symbols_accidental: t.Sequence[str],
        **kwargs,
    ) -> None:
        schema = PitchClassSchema(
            tuple(intervals),
            tuple(symbols_pitchclass),
            tuple(symbols_accidental),
        )
        super().__init_subclass__(schema=schema, **kwargs)

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
    def scale(self) -> _Scale | None:
        return self._scale

    @pitchname.setter
    def pitchname(self, name: str):
        if self.is_pitchname(name) and name in self._pitchnames:
            self._pitchname = name

    @scale.setter
    def scale(self, scale: _Scale | None):
        from ..scale import _Scale

        if isinstance(scale, _Scale):
            self._scale = scale
            pitchclass = (
                self.pitchclass - scale.key.pitchclass
            ) % self.schema.cardinality

            if (idx := index(scale.positions, pitchclass)) is not None:
                self._pitchname = self.schema.convert_pitchclass_to_pitchname(
                    self._pitchclass, scale.signatures[idx]
                )

    @classmethod
    def is_pitchname(cls, pitchname: t.Any) -> t.TypeGuard[str]:
        return cls.schema.is_pitchname(pitchname)

    @classmethod
    def is_pitchclass(cls, pitchclass: t.Any) -> t.TypeGuard[int]:
        return cls.schema.is_pitchclass(pitchclass)

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, (int, _PitchClassLike)):
            return NotImplemented
        return int(self) == int(other)

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: int | _PitchClassLike) -> t.Self:
        pitchclass = (int(self) + int(other)) % self.schema.cardinality
        return self.__class__(pitchclass, scale=self.scale, setting=self.setting)

    def __sub__(self, other: int | _PitchClassLike) -> t.Self:
        pitchclass = (int(self) - int(other)) % self.schema.cardinality
        return self.__class__(pitchclass, scale=self.scale, setting=self.setting)

    def __int__(self) -> int:
        return self._pitchclass

    def __str__(self) -> str:
        return f"<PitchClass: {self.pitchname or self.pitchnames}, scale: {self.scale}>"

    def __repr__(self) -> str:
        return f"<PitchClass: {self.pitchname or self.pitchnames}, scale: {self.scale}>"
