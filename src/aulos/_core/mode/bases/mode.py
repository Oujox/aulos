import typing as t
from itertools import starmap
from typing import cast

from aulos._core.context import inject
from aulos._core.mode import ModeSchema
from aulos._core.object import AulosSchemaObject
from aulos._core.pitchclass import BaseKey, BasePitchClass
from aulos._core.scale import BaseScale
from aulos._core.utils import Intervals, Positions, classproperty


class BaseMode[KEY: BaseKey, PITCHCLASS: BasePitchClass](AulosSchemaObject[ModeSchema]):
    _Key: t.ClassVar[type[BaseKey]]
    _PitchClass: t.ClassVar[type[BasePitchClass]]
    _intervals: t.ClassVar[Intervals]
    _positions: t.ClassVar[Positions]
    _base: t.ClassVar[type[BaseScale]]

    _key: KEY
    _signatures: tuple[int, ...]

    @inject
    def __init__(self, key: str | KEY, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)

        if isinstance(key, str):
            self._key = self.Key(key, setting=self._setting)
            self._signatures = tuple(
                starmap(
                    lambda x, y: x + y,
                    zip(
                        self._key.signature,
                        self.schema.scale.generate_scale_signatures(self._intervals),
                        strict=False,
                    ),
                ),
            )

        elif isinstance(key, BaseKey):
            self._key = key
            self._signatures = tuple(
                starmap(
                    lambda x, y: x + y,
                    zip(
                        self._key.signature,
                        self.schema.scale.generate_scale_signatures(self._intervals),
                        strict=False,
                    ),
                ),
            )

        else:
            raise TypeError

    def __init_subclass__(cls, *, base: type[BaseScale], shift: int, key: type[KEY]) -> None:
        schema = ModeSchema(base.schema)
        super().__init_subclass__(schema=schema)
        cls._Key = key
        cls._PitchClass = key.PitchClass
        cls._intervals = Intervals(base.intervals).left(shift)
        cls._positions = cls._intervals.to_positions()

    @classproperty
    def Key(self) -> type[KEY]:  # noqa: N802
        return cast("type[KEY]", self._Key)

    @classproperty
    def PitchClass(self) -> type[PITCHCLASS]:  # noqa: N802
        return cast("type[PITCHCLASS]", self._PitchClass)

    @classproperty
    def intervals(self) -> Intervals:
        return self._intervals

    @classproperty
    def positions(self) -> Positions:
        return self._positions

    @classproperty
    def base(self) -> type[BaseScale]:
        return self._base

    @property
    def key(self) -> KEY:
        return self._key

    @property
    def signatures(self) -> tuple[int, ...]:
        return self._signatures

    @property
    def components(self) -> tuple[PITCHCLASS, ...]:
        components = []
        root = self.PitchClass(self._key.keyname, scale=self, setting=self.setting)
        for pos in self.positions:
            pitchclass = (root + pos).pitchclass
            note = self.PitchClass(pitchclass, scale=self, setting=self.setting)
            components.append(note)
        return tuple(components)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseScale):
            return NotImplemented
        return self._intervals == other._intervals and self._key == other._key

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self._key}>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self._key}>"
