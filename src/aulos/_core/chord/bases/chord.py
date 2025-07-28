from __future__ import annotations

import typing as t
from typing import TYPE_CHECKING, cast

from aulos._core.context import inject
from aulos._core.note import BaseNote, NoteCollection
from aulos._core.object import AulosSchemaObject
from aulos._core.utils import Intervals, Positions, classproperty

from ..schemas import ChordSchema

if TYPE_CHECKING:
    from aulos._core.chord.quality import Quality, QualityProperty  # pragma: no cover
    from aulos._core.mode import BaseMode  # pragma: no cover
    from aulos._core.scale import BaseScale  # pragma: no cover
    from aulos._core.tuner import BaseTuner  # pragma: no cover


class BaseChord[NOTE: BaseNote](AulosSchemaObject[ChordSchema]):
    """
    Represents a musical chord, which is a combination of notes played simultaneously.

    This class extends the BaseChord and provides specific qualities and positions for various chord types,
    including triads, seventh chords, and altered chords. It allows for the representation and manipulation
    of chords in a musical context, using the Note class for individual notes.
    """

    _Note: t.ClassVar[type[BaseNote]]

    _root: NOTE
    _base: NOTE | None
    _quality: Quality
    _tuner: BaseTuner | None
    _scale: BaseScale | BaseMode | None

    @inject
    def __init__(
        self,
        identify: tuple[str, int],
        *,
        tuner: BaseTuner | None = None,
        scale: BaseScale | BaseMode | None = None,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(**kwargs)

        if isinstance(identify, tuple) and isinstance(identify[0], str) and isinstance(identify[1], int):
            if (parsed := self.schema.parse(identify[0])) is not None:
                root_notename, base_notename = self.schema.convert_to_chord_notenames(
                    parsed.root,
                    parsed.base,
                    identify[1],
                )

                if base_notename is None:
                    self._root = self.Note(root_notename)
                    self._base = None
                    self._quality = parsed.quality
                    self._tuner = tuner
                    self._scale = scale

                else:
                    self._root = self.Note(root_notename)
                    self._base = self.Note(base_notename)
                    self._quality = parsed.quality.from_base(self._base.notenumber - self._root.notenumber)
                    self._tuner = tuner
                    self._scale = scale

        else:
            raise TypeError

    def __init_subclass__(cls, qualities: t.Sequence[QualityProperty], note: type[NOTE]) -> None:
        schema = ChordSchema(
            tuple(qualities),
            note.schema,
        )
        super().__init_subclass__(schema=schema)
        cls._Note = note

    @classproperty
    def Note(self) -> type[NOTE]:  # noqa: N802
        return cast("type[NOTE]", self._Note)

    @property
    def root(self) -> NOTE:
        return self._root

    @property
    def quality(self) -> Quality:
        return self._quality

    @property
    def base(self) -> NOTE | None:
        return self._base

    @property
    def tuner(self) -> BaseTuner | None:
        """Returns the tuner of the note."""
        return self._tuner

    @property
    def scale(self) -> BaseScale | BaseMode | None:
        """Returns the scale of the note."""
        return self._scale

    @property
    def intervals(self) -> Intervals:
        return self._quality.intervals

    @property
    def positions(self) -> Positions:
        return self._quality.positions

    @property
    def components(self) -> NoteCollection[NOTE]:
        components = []
        if isinstance(self._base, BaseNote) and self._quality.is_onchord():
            components.append(
                self.Note(
                    self._base,
                    tuner=self._tuner,
                    scale=self._scale,
                    setting=self._setting,
                ),
            )
        components.extend(
            self.Note(
                int(self._root) + q,
                tuner=self._tuner,
                scale=self._scale,
                setting=self._setting,
            )
            for q in self._quality
        )
        return NoteCollection(components)

    def inverse(self, num: int = 1) -> None:
        self._quality = self._quality.inverse(num)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseChord):
            return NotImplemented
        return self.root == other.root and self.quality == other.quality and self.base == other.base

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"<Chord: {self.root}{self.quality.name}{self.base}>"

    def __repr__(self) -> str:
        return f"<Chord: {self.root}{self.quality.name}{self.base}>"
