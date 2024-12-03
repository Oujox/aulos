import typing as t
from functools import cached_property
from itertools import accumulate, compress

from .._core import Object
from .._core.context import inject
from .._core.utils import classproperty, rotate
from ..note import Key, PitchClass
from ._base import BaseScale
from .processing.accidentals import accidentals
from .scale import Scale


class Mode(BaseScale, Object):

    _intervals: t.ClassVar[tuple[int]]
    _shift: t.ClassVar[int]
    _scale: t.ClassVar[Scale]

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is Mode:
            raise TypeError("Mode cannot be instantiated directly.")
        return super().__new__(cls)

    @inject
    def __init__(self, key: Key, **kwargs) -> None:
        super().__init__(**kwargs)
        self._key = key

    def __init_subclass__(cls, shift: int, scale: Scale) -> None:
        cls._shift = -shift
        cls._scale = scale
        cls._intervals = tuple(rotate(cls._scale.intervals, cls._shift))
        return super().__init_subclass__(semitone=sum(cls._intervals))

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
        _accidentals = accidentals(self.schema.intervals, self._intervals)
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
        return "<Mode: {}>".format(self.__class__.__name__)

    def __repr__(self) -> str:
        return "<Mode: {}>".format(self.__class__.__name__)
