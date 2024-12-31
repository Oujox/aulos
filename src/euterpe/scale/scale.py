import typing as t
from itertools import accumulate

from .._core import EuterpeObject
from .._core.utils import classproperty
from ..note import Key, PitchClass
from ._base import BaseScale


class Scale(BaseScale, EuterpeObject):

    _intervals: t.ClassVar[tuple[int, ...]]
    _key: Key

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is Scale:
            raise TypeError("Scale cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, key: Key, **kwargs) -> None:
        super().__init__(**kwargs)
        self._key = key

    def __init_subclass__(cls, /, intervals: t.Sequence[int], **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        cls._intervals = tuple(intervals)

    @property
    def key(self) -> Key:
        return self._key

    @classproperty
    def intervals(cls) -> tuple[int, ...]:
        return cls._intervals

    @classproperty
    def positions(cls) -> tuple[int, ...]:
        return tuple(accumulate((0,) + cls._intervals[:-1]))

    @property
    def accidentals(self) -> tuple[int, ...]:
        _accidentals = self.schema.generate_scale_accidentals(self._intervals)
        return tuple(_accidentals)

    @property
    def diatonics(self) -> list[PitchClass]:
        diatonics = []
        root = PitchClass(self._key.pitchname, scale=self, setting=self.setting)
        for pos in self.positions:
            pitchclass = (root + pos).pitchclass
            note = PitchClass(pitchclass, scale=self, setting=self.setting)
            diatonics.append(note)
        return diatonics

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, Scale):
            return NotImplemented
        return self._intervals == other._intervals and self._key == other._key

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return "<Scale: {}>".format(self.__class__.__name__)

    def __repr__(self) -> str:
        return "<Scale: {}>".format(self.__class__.__name__)
