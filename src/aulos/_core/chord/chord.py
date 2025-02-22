from __future__ import annotations

import typing as t
from typing import TYPE_CHECKING

from aulos._core import AulosObject
from aulos._core.note import BaseNote

from .schemas import ChordSchema

if TYPE_CHECKING:
    from aulos._core.scale import Scale
    from aulos._core.tuner import Tuner

    from .quality import Quality, QualityProperty


class BaseChord[NOTE: BaseNote](AulosObject[ChordSchema]):
    Note: type[NOTE]

    _root: NOTE
    _on: NOTE | None
    _quality: Quality
    _tuner: Tuner | None
    _scale: Scale | None

    def __init__(
        self,
        name: str,
        *,
        octave: int | None = None,
        tuner: Tuner | None = None,
        scale: Scale | None = None,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)

        if (parsed := self.schema.parse(name)) is not None:
            root_notename = self.schema.note.convert_pitchname_to_notename(
                parsed.root, octave or self.Note.octave_default
            )
            self._root = self.Note(root_notename)
            self._quality = parsed.quality
            self._tuner = tuner
            self._scale = scale

            if parsed.on is not None:
                on_notename = self.schema.note.find_nearest_notename(root_notename, parsed.on, "down") or ""
                self._on = self.Note(on_notename)
                self._quality = self._quality.inverse_from_on(self._on.notenumber - self._root.notenumber)

            else:
                self._on = None

        else:
            raise TypeError

    def __init_subclass__(cls, qualities: t.Sequence[QualityProperty], note: type[NOTE]) -> None:
        schema = ChordSchema(
            tuple(qualities),
            note.schema,
        )
        super().__init_subclass__(schema=schema)
        cls.Note = note

    @property
    def root(self) -> NOTE:
        return self._root

    @property
    def quality(self) -> Quality:
        return self._quality

    @property
    def on(self) -> NOTE | None:
        return self._on

    @property
    def tuner(self) -> Tuner | None:
        """Returns the tuner of the note."""
        return self._tuner

    @property
    def scale(self) -> Scale | None:
        """Returns the scale of the note."""
        return self._scale

    @property
    def intervals(self) -> tuple[int, ...]:
        return tuple(self._quality.intervals)

    @property
    def positions(self) -> tuple[int, ...]:
        return tuple(self._quality.positions)

    @property
    def components(self) -> tuple[NOTE, ...]:
        return tuple(
            self.Note(
                int(self._on or self._root) + p,
                tuner=self._tuner,
                scale=self._scale,
                setting=self._setting,
            )
            for p in self._quality.positions
        )

    def inverse(self, num: int = 1) -> None:
        self._quality = self._quality.inverse(num)

    @classmethod
    def is_chord(cls, name: object) -> t.TypeGuard[str]:
        return cls.schema.is_chord(name)

    @classmethod
    def is_onchord(cls, name: object) -> t.TypeGuard[str]:
        return cls.schema.is_onchord(name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseChord):
            return NotImplemented
        return self.root == other.root and self.quality == other.quality and self.on == other.on

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"<Chord: {self.root}{self.quality.name}{self.on}>"

    def __repr__(self) -> str:
        return f"<Chord: {self.root}{self.quality.name}{self.on}>"
