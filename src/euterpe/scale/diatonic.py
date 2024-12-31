import typing as t
from itertools import pairwise

from .._core.utils import rotated
from ..note import Key
from .scale import Scale


class DiatonicScale(Scale, intervals=()):

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is DiatonicScale:
            raise TypeError("DiatonicScale cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, key: Key, **kwargs) -> None:
        super().__init__(key, **kwargs)

    def __init_subclass__(
        cls, /, intervals: t.Sequence[int], shift: int = 0, **kwargs
    ) -> None:
        super().__init_subclass__(intervals=rotated(intervals, shift), **kwargs)

    def __str__(self) -> str:
        return "<DiatonicScale: {}>".format(self.__class__.__name__)

    def __repr__(self) -> str:
        return "<DiatonicScale: {}>".format(self.__class__.__name__)


class NondiatonicScale(Scale, intervals=()):

    _extensions: t.ClassVar[tuple[tuple[int, ...], ...]]
    _base: t.ClassVar[type[Scale]]

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is NondiatonicScale:
            raise TypeError("NondiatonicScale cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, key: Key, **kwargs) -> None:
        super().__init__(key, **kwargs)

    def __init_subclass__(
        cls, /, extensions: t.Sequence[t.Sequence[int]], base: type[Scale], **kwargs
    ) -> None:
        cls._base = base
        cls._extensions = tuple(tuple(inner) for inner in extensions)
        _positions = tuple(
            d + nd for d, nds in zip(base.positions, cls._extensions) for nd in nds
        )
        _intervals = tuple(
            b - a for a, b in pairwise(_positions + (sum(base.intervals),))
        )
        super().__init_subclass__(intervals=_intervals, **kwargs)

    @property
    def accidentals(self) -> tuple[int, ...]:
        _accidentals = self.schema.generate_scale_accidentals(self._base.intervals)
        _accidentals = tuple(
            d + nd for d, nds in zip(_accidentals, self._extensions) for nd in nds
        )
        return _accidentals

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, NondiatonicScale):
            return NotImplemented
        return self._intervals == other._intervals and self._key == other._key

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return "<NondiatonicScale: {}>".format(self.__class__.__name__)

    def __repr__(self) -> str:
        return "<NondiatonicScale: {}>".format(self.__class__.__name__)
