from __future__ import annotations

import typing as t

from .._core import EuterpeObject
from ._base import BaseChord
from ..note import PitchClass
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

    _root: PitchClass
    _quality: Quality
    _on: PitchClass | None

    def __init__(self, identify: str, **kwargs):
        super().__init__(**kwargs)

        if (parsed := parse(identify, self)) is not None:
            root = PitchClass(parsed["root"], setting=self.setting)
            on = PitchClass(parsed["on"], setting=self.setting) if parsed["on"] is not None else None
            self._root = root
            self._quality = parsed["quality"]
            self._on = on

        else:
            raise ValueError()

    @property
    def root(self) -> PitchClass:
        return self._root

    @property
    def quality(self) -> Quality:
        return self._quality

    @property
    def on(self) -> PitchClass | None:
        return self._on
    
    @property
    def positions(self) -> tuple[int, ...]:
        return self._quality.intervals
    
    @property
    def components(self) -> tuple[PitchClass, ...]:
        return ()
    
    def invert(self, inversion: int) -> Chord:
        ...
    
    def transpose(self, interval: int) -> Chord:
        ...
    
    def is_inverted(self) -> bool:
        ...
