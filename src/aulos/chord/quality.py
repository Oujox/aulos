import typing as t
from dataclasses import dataclass


class _OptionalQualityProperty(t.TypedDict, total=False):
    areas: tuple[str, ...]


class _RequiredQualityProperty(t.TypedDict, total=True):
    name: str
    positions: tuple[int, ...]


class QualityProperty(_RequiredQualityProperty, _OptionalQualityProperty):
    """ """


@dataclass(frozen=True, slots=False)
class Quality:
    name: str
    areas: tuple[str, ...]
    positions: tuple[int, ...]
