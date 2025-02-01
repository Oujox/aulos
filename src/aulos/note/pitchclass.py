import typing as t
from typing import TYPE_CHECKING

from aulos._core import AulosObject
from aulos._core.utils import index

from .schemas import PitchClassSchema

if TYPE_CHECKING:
    from aulos.scale import Scale  # pragma: no cover


def resolve_pitchname_from_scale(pitchclass: int, scale: "Scale | None", schema: PitchClassSchema) -> str | None:
    if scale is not None:
        relative_pitchclass = (pitchclass - int(scale.key)) % schema.cardinality
        if (idx := index(scale.positions, relative_pitchclass)) is not None:
            return schema.convert_pitchclass_to_pitchname(
                pitchclass,
                scale.signatures[idx],
            )
    return None


class BasePitchClass(AulosObject[PitchClassSchema]):
    _pitchclass: int
    _pitchnames: tuple[str | None, ...]
    _pitchname: str | None
    _scale: "Scale | None"

    def __init__(
        self,
        identify: int | str | t.Self,
        *,
        scale: "Scale | None" = None,
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

    @property
    def scale(self) -> "Scale | None":
        return self._scale

    @classmethod
    def is_pitchname(cls, pitchname: object) -> t.TypeGuard[str]:
        return cls.schema.is_pitchname(pitchname)

    @classmethod
    def is_pitchclass(cls, pitchclass: object) -> t.TypeGuard[int]:
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
