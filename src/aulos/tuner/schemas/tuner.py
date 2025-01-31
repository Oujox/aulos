from dataclasses import dataclass

from ..._core import Schema
from ...note.schemas import NoteSchema, PitchClassSchema


@dataclass(frozen=True)
class TunerSchema(Schema):
    reference_notenumber: int
    note: NoteSchema
    pitchclass: PitchClassSchema

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        # [check] reference_notenumber
        if self.reference_notenumber not in self.note.notenumbers:
            raise Exception
