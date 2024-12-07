import typing as t
from functools import cached_property
from itertools import accumulate, compress

from .._core import AulosObject
from .._core.context import inject
from .._core.utils import classproperty, rotate
from ..note import Key, PitchClass
from ._base import BaseScale
from .processing.accidentals import accidentals


class Scale(BaseScale, AulosObject):

    _intervals: t.ClassVar[tuple[int]]

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is Scale:
            raise TypeError("Scale cannot be instantiated directly.")
        return super().__new__(cls)

    @inject
    def __init__(self, key: Key, **kwargs) -> None:
        super().__init__(**kwargs)
        self._key = key

    def __init_subclass__(cls, intervals: t.Iterable[int]) -> None:
        cls._intervals = tuple(intervals)
        return super().__init_subclass__(intervals=cls.intervals)

    @property
    def key(self) -> Key:
        return self._key

    @classproperty
    def intervals(cls) -> tuple[int]:
        return tuple(compress(cls._intervals, cls.omits))

    @classproperty
    def positions(cls) -> tuple[int]:
        _intervals = (0,) + cls._intervals[:-1]
        _positions = tuple(accumulate(_intervals))
        return tuple(compress(_positions, cls.omits))

    @classproperty
    def omits(cls) -> tuple[bool]:
        _intervals = (1,) + cls._intervals[:-1]
        return tuple([bool(i) for i in _intervals])

    @cached_property
    def accidentals(self) -> tuple[int]:
        _accidentals = accidentals(self.logic.intervals, self._intervals)
        return tuple(compress(_accidentals, self.omits))

    @cached_property
    def diatonics(self) -> list[PitchClass]:
        diatonics = []
        root = PitchClass(self._key.pitchname, scale=self, setting=self.setting)
        for pos in self.positions:
            pitchclass = (root + pos).pitchclass
            note = PitchClass(pitchclass, scale=self, setting=self.setting)
            diatonics.append(note)
        return diatonics

    def __eq__(self, other: t.Self) -> bool:
        return self._intervals == other._intervals and self.key == other.key

    def __ne__(self, other: t.Self) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return "<Scale: {}>".format(self.__class__.__name__)

    def __repr__(self) -> str:
        return "<Scale: {}>".format(self.__class__.__name__)
