from dataclasses import dataclass

from aulos._core.note import NoteSchema
from aulos._core.pitchclass import PitchClassSchema
from aulos._core.schema import Schema


@dataclass(init=False, frozen=True, slots=True)
class TunerSchema(Schema):
    reference_notenumber: int
    note: NoteSchema
    pitchclass: PitchClassSchema

    def __init__(self, /, reference_notenumber: int, note: NoteSchema, pitchclass: PitchClassSchema) -> None:
        super(Schema, self).__init__()
        object.__setattr__(self, "reference_notenumber", reference_notenumber)
        object.__setattr__(self, "note", note)
        object.__setattr__(self, "pitchclass", pitchclass)

    def validate(self) -> None:
        pass
