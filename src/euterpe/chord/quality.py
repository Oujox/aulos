from __future__ import annotations

import typing as t

from .._core.framework import DerivedCacheMeta
from .._core.utils import classproperty


def parse_quality(name: str) -> type[Quality] | None:
    for q in Quality._derived_cache:
        if name == q.name:
            return q
        if name in q.areas:
            return q
    return None


class Quality(metaclass=DerivedCacheMeta):
    _name: t.ClassVar[str]
    _areas: t.ClassVar[tuple[str, ...]]
    _positions: t.ClassVar[tuple[int, ...]]

    def __init_subclass__(
        cls,
        *,
        name: str,
        areas: tuple[str, ...],
        positions: tuple[int, ...],
        **kwargs,
    ) -> None:
        super().__init_subclass__(**kwargs)
        cls._name = name
        cls._areas = areas
        cls._positions = positions

    @classproperty
    def name(cls) -> str:
        return cls._name

    @classproperty
    def areas(cls) -> tuple[str, ...]:
        return cls._areas

    @classproperty
    def positions(cls) -> tuple[int, ...]:
        return cls._positions
