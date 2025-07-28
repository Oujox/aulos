import typing as t
from dataclasses import dataclass
from functools import cached_property
from itertools import starmap

from aulos._core.schema import Schema

from .pitchclass import PitchClassSchema


@dataclass(init=False, frozen=True, slots=True)
class KeySchema(Schema):
    accidental: int
    pitchclass: PitchClassSchema

    def __init__(self, /, accidental: int, pitchclass: PitchClassSchema) -> None:
        super(Schema, self).__init__()
        object.__setattr__(self, "accidental", accidental)
        object.__setattr__(self, "pitchclass", pitchclass)

    def validate(self) -> None:
        pass

    @cached_property
    def keynames(self) -> tuple[str, ...]:
        keynames = [
            pitchname
            for pitchname in self.pitchclass.pitchnames
            if abs(self.pitchclass.get_accidental(pitchname)) <= self.accidental
        ]
        return tuple(keynames)

    def generate_key_signatures(self, keyname: str) -> tuple[int, ...]:
        self.ensure_valid_keyname(keyname)
        std_positions = self.pitchclass.standard_positions
        key_positions = self.pitchclass.get_positions(keyname)
        return tuple(
            starmap(
                lambda x, y: x - y,
                zip(std_positions, key_positions, strict=False),
            ),
        )

    def is_keyname(self, value: object) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.keynames

    def ensure_valid_keyname(self, keyname: str) -> None:
        if not self.is_keyname(keyname):
            raise ValueError
