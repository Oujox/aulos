import typing as t
from typing import TYPE_CHECKING

from aulos._core import AulosObject
from aulos._core.utils import index

from .pitchclass import BasePitchClass
from .schemas import NoteSchema

if TYPE_CHECKING:
    from aulos.scale import Scale  # pragma: no cover
    from aulos.tuner import Tuner  # pragma: no cover


def resolve_notename_from_scale(notenumber: int, scale: "Scale | None", schema: NoteSchema) -> str | None:
    if scale is not None:
        relative_pitchclass = schema.convert_notenumber_to_pitchclass(notenumber)
        relative_pitchclass = (relative_pitchclass - int(scale.key)) % schema.pitchclass.cardinality
        if (idx := index(scale.positions, relative_pitchclass)) is not None:
            return schema.convert_notenumber_to_notename(
                notenumber,
                scale.signatures[idx],
            )
    return None


class BaseNote[PITCHCLASS: BasePitchClass](AulosObject[NoteSchema]):
    PitchClass: type[PITCHCLASS]
    _notenumber: int
    _notenames: tuple[str | None, ...]
    _notename: str | None
    _tuner: "Tuner | None"
    _scale: "Scale | None"

    def __init__(
        self,
        identify: int | str,
        *,
        tuner: "Tuner | None" = None,
        scale: "Scale | None" = None,
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
        reference_notenumber: int,
        reference_octave: int,
        pitchclass: type[PITCHCLASS],
        **kwargs: t.Any,
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

    @property
    def tuner(self) -> "Tuner | None":
        return self._tuner

    @property
    def scale(self) -> "Scale | None":
        return self._scale

    @property
    def hz(self) -> float | None:
        if self._tuner is None:
            return None
        return self._tuner.hz(self._notenumber)

    def to_pitchclass(self) -> PITCHCLASS:
        pitchlass = self.schema.convert_notenumber_to_pitchclass(self._notenumber)
        return self.PitchClass(
            pitchlass,
            tuner=self._tuner,
            scale=self._scale,
            setting=self._setting,
        )

    @classmethod
    def is_notename(cls, notename: object) -> t.TypeGuard[str]:
        return cls.schema.is_notename(notename)

    @classmethod
    def is_notenumber(cls, notenumber: object) -> t.TypeGuard[int]:
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
            scale=self.scale,
            setting=self.setting,
        )

    def __sub__(self, other: t.SupportsInt) -> t.Self:
        return self.__class__(
            int(self) - int(other),
            scale=self.scale,
            setting=self.setting,
        )

    def __int__(self) -> int:
        return self._notenumber

    def __str__(self) -> str:
        return f"<Note: {self.notename or self.notenames}, scale: {self.scale}>"

    def __repr__(self) -> str:
        return f"<Note: {self.notename or self.notenames}, scale: {self.scale}>"
