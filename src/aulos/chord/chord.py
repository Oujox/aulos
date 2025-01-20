from __future__ import annotations

import typing as t

from .._core import AulosObject
from ..note import _PitchClass
from .quality import Quality, parse_quality


class _IChord(t.TypedDict):
    root: str
    quality: type[Quality]
    on: str | None


def parse_chord(name: str, instance: Chord) -> _IChord | None:
    if (root := instance.schema.find_pitchname(name)) is None:
        return None

    rest = name.replace(root, "", 1)
    if rest.find("/") >= 0:
        quality, on = rest.split("/", 1)
        quality = parse_quality(quality)
        on = instance.schema.find_pitchname(on)
    else:
        quality = parse_quality(rest)
        on = None

    if quality is None:
        return None

    return {"root": root, "on": on, "quality": quality}


class Chord(AulosObject):

    _root: _PitchClass
    _quality: Quality
    _on: _PitchClass | None

    def __init__(self, identify: str, **kwargs):
        super().__init__(**kwargs)

        if (parsed := parse_chord(identify, self)) is not None:
            root = _PitchClass(parsed["root"], setting=self.setting)
            quality = parsed["quality"]()
            on = (
                _PitchClass(parsed["on"], setting=self.setting)
                if parsed["on"] is not None
                else None
            )
            self._root = root
            self._quality = quality
            self._on = on

        else:
            raise ValueError()

    @property
    def root(self) -> _PitchClass:
        return self._root

    @property
    def quality(self) -> Quality:
        return self._quality

    @property
    def on(self) -> _PitchClass | None:
        return self._on

    @property
    def positions(self) -> tuple[int, ...]:
        return self._quality.positions

    @property
    def components(self) -> tuple[_PitchClass, ...]:
        return ()

    def invert(self, inversion: int) -> Chord: ...

    def transpose(self, interval: int) -> Chord: ...

    def is_inverted(self) -> bool: ...
