from __future__ import annotations

import typing as t

from .._core import EuterpeObject
from ._base import BaseChord
from .quality import Quality


class _IChord(t.TypedDict):
    root: str
    quality: Quality
    on: str | None


def parse(name: str, instance: Chord) -> _IChord | None:
    if (root := instance.schema.find_pitchname(name)) is None:
        return None

    rest = name.replace(root, "", 1)
    if rest.find("/") >= 0:
        quality, on = rest.split("/", 1)
        quality = instance.schema.name2quality.get(quality, None)
        on = instance.schema.find_pitchname(on)
    else:
        quality = instance.schema.name2quality.get(rest, None)
        on = None

    if quality is None:
        return None

    return {"root": root, "on": on, "quality": quality}


class Chord(BaseChord, EuterpeObject):

    _root: str
    _quality: Quality
    _on: str | None

    def __init__(self, identify: str, **kwargs):
        super().__init__(**kwargs)

        if (parsed := parse(identify, self)) is not None:
            self._root = parsed["root"]
            self._quality = parsed["quality"]
            self._on = parsed["on"]

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
