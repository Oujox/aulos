import typing as t
from dataclasses import dataclass

from aulos._core import Schema
from aulos.chord.quality import Quality


@dataclass(frozen=True, slots=True)
class ChordSchema(Schema):
    qualities: tuple[Quality, ...]

    def __post_init__(self) -> None:
        self.validate()

    def initialize(self) -> None:
        pass

    def validate(self) -> None:
        pass

    def is_chordname(self, chordname: object) -> t.TypeGuard[str]:
        return isinstance(chordname, str)
