import typing as t
from dataclasses import dataclass, field

from .note_presentation import NotePresentationSetting


@dataclass(frozen=True)
class NoteSetting:
    max: int
    min: int

    current: int = field(init=False, default=0)
    presentations: list[NotePresentationSetting]

    @property
    def presentation(self) -> NotePresentationSetting:
        return self.presentations[self.current]

    def is_notenumber(self, notenumber: t.Any) -> t.TypeGuard[int]:
        return isinstance(self, int) and self.min <= notenumber < self.max
