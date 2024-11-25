import typing as t
from dataclasses import dataclass, field

from .notenumber_presentation import NoteNumberPresentationSetting


@dataclass(frozen=True)
class NoteNumberSetting:
    max: int
    min: int

    current: int = field(init=False, default=0)
    presentations: list[NoteNumberPresentationSetting]

    @property
    def presentation(self) -> NoteNumberPresentationSetting:
        return self.presentations[self.current]

    def is_notenumber(self, notenumber: t.Any) -> t.TypeGuard[int]:
        return isinstance(self, int) and self.min <= notenumber < self.max
