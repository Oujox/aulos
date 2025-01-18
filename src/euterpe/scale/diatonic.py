import typing as t
from itertools import pairwise

from .._core.utils import classproperty, rotated
from ..note import _Key
from ..note import _PitchClass
from .scale import _Scale


class _DiatonicScale[T: _PitchClass](_Scale[T]):

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is _DiatonicScale:
            raise TypeError("DiatonicScale cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, key: _Key, **kwargs) -> None:
        super().__init__(key, **kwargs)

    def __init_subclass__(
        cls,
        *,
        intervals: t.Sequence[int],
        shift: int = 0,
        pitchclass: type[T],
        **kwargs,
    ) -> None:
        super().__init_subclass__(
            intervals=rotated(intervals, -shift),
            pitchclass=pitchclass,
            **kwargs,
        )


class _NondiatonicScale[T: _PitchClass](_Scale[T]):

    _extensions: t.ClassVar[tuple[tuple[int, ...], ...]]
    _base: t.ClassVar[type[_Scale]]

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is _NondiatonicScale:
            raise TypeError("NondiatonicScale cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, key: _Key, **kwargs) -> None:
        super().__init__(key, **kwargs)

    def __init_subclass__(
        cls,
        *,
        extensions: t.Sequence[t.Sequence[int]],
        base: type[_DiatonicScale],
        pitchclass: type[T],
        **kwargs,
    ) -> None:
        super().__init_subclass__(
            intervals=base.intervals,
            pitchclass=pitchclass,
            **kwargs,
        )
        cls._base = base
        cls._extensions = tuple(tuple(inner) for inner in extensions)

    @classproperty
    def intervals(cls) -> tuple[int, ...]:
        intervals = tuple(
            b - a for a, b in pairwise(cls.positions + (sum(super().intervals),))
        )
        return intervals

    @classproperty
    def positions(cls) -> tuple[int, ...]:
        positions = tuple(
            pos + ext
            for pos, exts in zip(super().positions, cls._extensions)
            for ext in exts
        )
        return positions

    @property
    def signatures(self) -> tuple[int, ...]:
        signatures = tuple(
            sig + ext
            for sig, exts in zip(super().signatures, self._extensions)
            for ext in exts
        )
        return signatures
