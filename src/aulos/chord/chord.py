import typing as t

from .._core import AulosObject
from ._base import BaseChord
from .quality import Quality


class Chord(BaseChord, AulosObject):

    _root: str
    _quality: Quality
    _on: str | None

    def __init__(self, identify: str, **kwargs):
        super().__init__(**kwargs)

        parsed = self.schema.parse_chord(identify)
        root = parsed["root"]
        on = parsed["on"]
        quality = parsed["quality"]

        if all([root, quality]):
            self._root = root
            self._quality = quality
            self._on = on

        else:
            raise ValueError()

    @property
    def root(self) -> str:
        return self._root

    @property
    def quality(self) -> Quality:
        return self._quality

    @property
    def on(self) -> str | None:
        return self._on

    def is_chord(self, chord: t.Any) -> t.TypeGuard[str]:
        matched = self.schema.find_pitchname(chord)
        return isinstance(chord, str) and matched is not None
