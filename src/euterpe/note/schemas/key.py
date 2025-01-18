import typing as t
from dataclasses import dataclass
from functools import cached_property

from ..._core import Schema
from ..._core.utils import wrapped_diff
from .pitchclass import PitchClassSchema


@dataclass(frozen=True, slots=True)
class KeySchema(Schema):

    accidental: int
    pitchclass: PitchClassSchema

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        # [check] accidental
        if not self.accidental > 0:
            raise Exception()
        if not self.accidental < self.pitchclass.accidental:
            raise Exception()

    @cached_property
    def keynames(self) -> tuple[str, ...]:
        keynames = [
            pitchname
            for pitchname in self.pitchclass.pitchnames
            if abs(self.pitchclass.count_accidental(pitchname)) <= self.accidental
        ]
        return tuple(keynames)

    def generate_key_signatures(self, keyname: str) -> tuple[int, ...]:
        self.ensure_valid_keyname(keyname)
        positions = []
        r_symbol = self.pitchclass.convert_pitchname_to_symbol(keyname)
        r_pitchclass = self.pitchclass.convert_pitchname_to_picthclass(keyname)

        idx = self.pitchclass.symbols_pitchclass.index(r_symbol)
        symbols = (
            self.pitchclass.symbols_pitchclass[idx:]
            + self.pitchclass.symbols_pitchclass[:idx]
        )

        for pos, symbol in zip(self.pitchclass.positions, symbols):
            n_pos = self.pitchclass.convert_pitchname_to_picthclass(symbol)
            a_pos = (r_pitchclass + pos) % self.pitchclass.cardinality
            positions.append(wrapped_diff(a_pos, n_pos, self.pitchclass.cardinality))
        return tuple(positions)

    def is_keyname(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.keynames

    def ensure_valid_keyname(self, keyname: str) -> None:
        if not self.is_keyname(keyname):
            raise ValueError()
