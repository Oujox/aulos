import typing as t
from functools import cached_property
from itertools import accumulate, compress

from .._core import EuterpeObject
from .._core.utils import classproperty, rotate
from ..note import Key, PitchClass
from ._base import BaseScale
from .processing.accidentals import accidentals
from .scale import Scale


class Mode(BaseScale, EuterpeObject):

    _intervals: t.ClassVar[tuple[int]]
    _scale: t.ClassVar[Scale]
    _key: Key
    _accidentals: tuple[int]

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is Mode:
            raise TypeError("Mode cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, key: Key, **kwargs) -> None:
        super().__init__(**kwargs)
        self._key = key
        self._accidentals = self.schema.generate_scale_accidentals(self._intervals)

    def __init_subclass__(cls, scale: Scale, intervals: tuple[int], **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls._scale = scale
        cls._intervals = tuple(intervals)

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

    @property
    def accidentals(self) -> tuple[int]:
        return tuple(compress(self._accidentals, self.omits))

    @property
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
        return "<Mode: {}>".format(self.__class__.__name__)

    def __repr__(self) -> str:
        return "<Mode: {}>".format(self.__class__.__name__)
