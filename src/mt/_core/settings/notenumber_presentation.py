import typing as t
from dataclasses import dataclass


@dataclass(frozen=True)
class NoteNumberPresentationReferenceSetting:
    number: int
    symbol: int


@dataclass(frozen=True)
class NoteNumberPresentationSetting:
    name: str
    symbols: list[str]
    reference: NoteNumberPresentationReferenceSetting
