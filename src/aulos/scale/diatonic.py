import typing as t
from itertools import pairwise
from typing import TYPE_CHECKING

from aulos._core.utils import classproperty, rotated

from .scale import Scale

# type annotaion
if TYPE_CHECKING:
    from aulos.note import BaseKey, BasePitchClass


class DiatonicScale[KEY: BaseKey, PITCHCLASS: BasePitchClass](Scale[KEY, PITCHCLASS]):
    def __new__(cls, *_args: t.Any, **_kwargs: t.Any) -> t.Self:
        if cls is DiatonicScale:
            msg = "DiatonicScale cannot be instantiated directly."
            raise TypeError(msg)
        return super().__new__(cls)

    def __init_subclass__(
        cls,
        *,
        intervals: t.Sequence[int],
        shift: int = 0,
        key: type[KEY],
        **kwargs: t.Any,
    ) -> None:
        super().__init_subclass__(
            intervals=rotated(intervals, -shift),
            key=key,
            **kwargs,
        )


class NondiatonicScale[KEY: BaseKey, PITCHCLASS: BasePitchClass](
    Scale[KEY, PITCHCLASS],
):
    _extensions: t.ClassVar[tuple[tuple[int, ...], ...]]
    _base: t.ClassVar[type[Scale]]

    def __new__(cls, *_args: t.Any, **_kwargs: t.Any) -> t.Self:
        if cls is NondiatonicScale:
            msg = "NondiatonicScale cannot be instantiated directly."
            raise TypeError(msg)
        return super().__new__(cls)

    def __init_subclass__(
        cls,
        *,
        extensions: t.Sequence[t.Sequence[int]],
        base: type[DiatonicScale],
        key: type[KEY],
        **kwargs: t.Any,
    ) -> None:
        super().__init_subclass__(
            intervals=base.intervals,
            key=key,
            **kwargs,
        )
        cls._base = base
        cls._extensions = tuple(tuple(inner) for inner in extensions)

    @classproperty
    def intervals(self) -> tuple[int, ...]:
        return tuple(b - a for a, b in pairwise((*self.positions, sum(super().intervals))))

    @classproperty
    def positions(self) -> tuple[int, ...]:
        return tuple(pos + ext for pos, exts in zip(super().positions, self._extensions, strict=False) for ext in exts)

    @property
    def signatures(self) -> tuple[int, ...]:
        return tuple(sig + ext for sig, exts in zip(super().signatures, self._extensions, strict=False) for ext in exts)
