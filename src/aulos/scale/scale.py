import typing as t
from itertools import accumulate, starmap

from .._core import AulosObject
from .._core.utils import classproperty
from ..note import _Key, _PitchClass
from .schemas import ScaleSchema


class _Scale[T: _PitchClass](AulosObject[ScaleSchema]):

    PitchClass: type[T]
    _intervals: t.ClassVar[tuple[int, ...]]
    _positions: t.ClassVar[tuple[int, ...]]
    _key: _Key
    _signatures: tuple[int, ...]

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is _Scale:
            raise TypeError("Scale cannot be instantiated directly.")
        return super().__new__(cls)

    def __init__(self, key: _Key, **kwargs) -> None:
        super().__init__(**kwargs)
        self._key = key
        self._signatures = tuple(
            starmap(
                lambda x, y: x + y,
                zip(
                    self._key.signature,
                    self.schema.generate_scale_signatures(self._intervals),
                ),
            )
        )

    def __init_subclass__(
        cls,
        *,
        intervals: t.Sequence[int] | None = None,
        pitchclass: type[T] | None = None,
        **kwargs,
    ) -> None:
        if intervals is None or pitchclass is None:
            return
        schema = ScaleSchema(pitchclass.schema)
        super().__init_subclass__(schema=schema, **kwargs)
        cls.PitchClass = pitchclass
        cls._intervals = tuple(intervals)
        cls._positions = tuple(accumulate((0,) + cls._intervals[:-1]))

    @property
    def key(self) -> _Key:
        return self._key

    @classproperty
    def intervals(cls) -> tuple[int, ...]:
        return cls._intervals

    @classproperty
    def positions(cls) -> tuple[int, ...]:
        return cls._positions

    @property
    def signatures(self) -> tuple[int, ...]:
        return self._signatures

    @property
    def components(self) -> tuple[T, ...]:
        components = []
        root = self.PitchClass(self._key.pitchname, scale=self, setting=self.setting)
        for pos in self.positions:
            pitchclass = (root + pos).pitchclass
            note = self.PitchClass(pitchclass, scale=self, setting=self.setting)
            components.append(note)
        return tuple(components)

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, _Scale):
            return NotImplemented
        return self._intervals == other._intervals and self._key == other._key

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self._key}>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self._key}>"
