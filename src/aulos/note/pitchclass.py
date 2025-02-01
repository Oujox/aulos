import typing as t
from typing import TYPE_CHECKING

from aulos._core import AulosObject
from aulos._core.utils import index

from .schemas import PitchClassSchema

if TYPE_CHECKING:
    from aulos.scale import Scale  # pragma: no cover


class BasePitchClass(AulosObject[PitchClassSchema]):
    _pitchclass: int
    _pitchnames: tuple[str | None, ...]
    _pitchname: str | None
    _scale: t.Optional["Scale"]

    def __init__(
        self,
        identify: int | str | t.Self,
        *,
        scale: t.Optional["Scale"] = None,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)

        if isinstance(identify, BasePitchClass):
            self._pitchclass = identify._pitchclass
            self._pitchnames = identify._pitchnames
            self._pitchname = identify._pitchname
            self._scale = None
            self.scale = identify._scale

        elif self.is_pitchclass(identify):
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
            raise ValueError

    def __init_subclass__(
        cls,
        *,
        intervals: t.Sequence[int],
        symbols_pitchclass: t.Sequence[str],
        symbols_accidental: t.Sequence[str],
        **kwargs: t.Any,
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
    def pitchnames(self) -> list[str]:
        return [n for n in self._pitchnames if n is not None]

    @property
    def pitchname(self) -> str | None:
        return self._pitchname

    @pitchname.setter
    def pitchname(self, name: str) -> None:
        if self.is_pitchname(name) and name in self._pitchnames:
            self._pitchname = name

    @property
    def scale(self) -> t.Optional["Scale"]:
        return self._scale

    @scale.setter
    def scale(self, scale: t.Optional["Scale"]) -> None:
        from aulos.scale import Scale

        if isinstance(scale, Scale):
            self._scale = scale
            pitchclass = (int(self) - int(scale.key)) % self.schema.cardinality

            if (idx := index(scale.positions, pitchclass)) is not None:
                self._pitchname = self.schema.convert_pitchclass_to_pitchname(
                    self._pitchclass,
                    scale.signatures[idx],
                )

    @classmethod
    def is_pitchname(cls, pitchname: t.Any) -> t.TypeGuard[str]:
        return cls.schema.is_pitchname(pitchname)

    @classmethod
    def is_pitchclass(cls, pitchclass: t.Any) -> t.TypeGuard[int]:
        return cls.schema.is_pitchclass(pitchclass)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, t.SupportsInt):
            return NotImplemented
        return int(self) == int(other)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __add__(self, other: t.SupportsInt) -> t.Self:
        pitchclass = (int(self) + int(other)) % self.schema.cardinality
        return self.__class__(pitchclass, scale=self.scale, setting=self.setting)

    def __sub__(self, other: t.SupportsInt) -> t.Self:
        pitchclass = (int(self) - int(other)) % self.schema.cardinality
        return self.__class__(pitchclass, scale=self.scale, setting=self.setting)

    def __int__(self) -> int:
        return self._pitchclass

    def __str__(self) -> str:
        return f"<PitchClass: {self.pitchname or self.pitchnames}, scale: {self.scale}>"

    def __repr__(self) -> str:
        return f"<PitchClass: {self.pitchname or self.pitchnames}, scale: {self.scale}>"
