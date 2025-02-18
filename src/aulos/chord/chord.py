import typing as t

from aulos._core import AulosObject
from aulos.note import BaseNote

from .quality import Quality, QualityProperty
from .schemas import ChordSchema


class BaseChord[NOTE: BaseNote](AulosObject[ChordSchema]):
    Note: type[NOTE]
    _root: NOTE
    _quality: Quality
    _on: NOTE | None

    def __init__(self, name: str, *, octave: int | None = None, **kwargs: t.Any) -> None:
        super().__init__(**kwargs)

        if (parsed := self.schema.parse(name)) is not None:
            root_notename = self.schema.note.convert_pitchname_to_notename(
                parsed.root, octave or self.Note.octave_default
            )
            self._root = self.Note(root_notename)
            self._quality = parsed.quality

            if parsed.on is not None:
                on_notename = self.schema.note.find_nearest_notename(root_notename, parsed.on, "down")
                if on_notename is None:
                    raise TypeError

                self._on = self.Note(on_notename)
            else:
                self._on = None

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
    def intervals(self) -> tuple[int, ...]:
        return tuple(self._quality.intervals)

    @property
    def positions(self) -> tuple[int, ...]:
        return tuple(self._quality.positions)

    @property
    def components(self) -> tuple[NOTE, ...]:
        return ()

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
