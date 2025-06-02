from dataclasses import dataclass

from aulos._core.chord.quality import Quality, QualityProperty
from aulos._core.note import NoteSchema
from aulos._core.schema import Schema
from aulos._core.utils import Positions


@dataclass(frozen=True, slots=True)
class ChordComponents:
    root: str
    base: str | None
    quality: Quality


@dataclass(init=False, frozen=True, slots=True)
class ChordSchema(Schema):
    qualities: tuple[Quality, ...]
    name2quality: dict[str, Quality]
    quality2name: dict[Quality, str]
    note: NoteSchema

    def __init__(
        self,
        /,
        qualities_property: tuple[QualityProperty, ...],
        note: NoteSchema,
    ) -> None:
        super(Schema, self).__init__()

        def to_quality(quality: QualityProperty, cardinality: int) -> Quality:
            while not all(p < cardinality for p in quality["positions"]):
                cardinality *= 2
            positions = Positions(quality["positions"], cardinality)
            return Quality(
                name=quality["name"],
                positions=positions,
            )

        classes = note.pitchclass.classes
        qualities = tuple(to_quality(q, classes) for q in qualities_property)

        name2quality = {q.name: q for q in qualities}
        quality2name = {q: q.name for q in qualities}

        object.__setattr__(self, "qualities", qualities)
        object.__setattr__(self, "name2quality", name2quality)
        object.__setattr__(self, "quality2name", quality2name)
        object.__setattr__(self, "note", note)

    def validate(self) -> None:
        pass

    def parse(self, name: str) -> ChordComponents | None:
        if "/" not in name:
            root = self.note.pitchclass.find_pitchname(name)

            if root is None:
                return None

            rest = name.split(root, 1)[1]
            quality = self.name2quality[rest]
            return ChordComponents(root=root, quality=quality, base=None)
        root_quality, maybe_base = name.split("/", 1)
        base = self.note.pitchclass.find_pitchname(maybe_base)
        root = self.note.pitchclass.find_pitchname(root_quality)

        if root is None or base is None:
            return None

        rest = root_quality.split(root, 1)[1]
        quality = self.name2quality[rest]
        return ChordComponents(root=root, quality=quality, base=base)

    def convert_to_chord_notenames(
        self, root_pitchname: str, base_pitchname: str | None, octave: int
    ) -> tuple[str, str | None]:
        root_notename = self.note.convert_pitchname_to_notename(root_pitchname, octave)
        if base_pitchname is None:
            return (root_notename, None)
        base_notename = self.note.find_nearest_notename(root_notename, base_pitchname, "down")
        return (root_notename, base_notename)
