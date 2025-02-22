from dataclasses import dataclass

from aulos._core import Schema
from aulos._core.note.schemas import NoteSchema, PitchClassSchema
from aulos._errors import ValidationError


@dataclass(frozen=True)
class TunerSchema(Schema):
    reference_notenumber: int
    note: NoteSchema
    pitchclass: PitchClassSchema

    def __post_init__(self) -> None:
        self.validate()

    def initialize(self) -> None:
        pass

    def validate(self) -> None:
        # [check] reference_notenumber
        if self.reference_notenumber not in self.note.notenumbers:
            msg = ""
            raise ValidationError(msg)
