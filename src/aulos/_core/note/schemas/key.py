import typing as t
from dataclasses import dataclass
from functools import cached_property

from aulos._core.schema import Schema

from .pitchclass import PitchClassSchema


def cyclic_difference(lhs: int, rhs: int, cycle_length: int | None = None) -> int:
    if cycle_length is not None:
        result1 = lhs - rhs
        result2 = (lhs + (cycle_length if lhs < rhs else 0)) - (rhs + (cycle_length if lhs > rhs else 0))
        return result1 if abs(result1) < abs(result2) else result2
    return lhs - rhs


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
        positions = []
        r_symbol = self.pitchclass.convert_pitchname_to_symbol(keyname)
        r_pitchclass = self.pitchclass.convert_pitchname_to_picthclass(keyname)

        idx = self.pitchclass.symbols_pitchclass.index(r_symbol)
        symbols = self.pitchclass.symbols_pitchclass[idx:] + self.pitchclass.symbols_pitchclass[:idx]

        for pos, symbol in zip(self.pitchclass.standard_positions, symbols, strict=False):
            n_pos = self.pitchclass.convert_pitchname_to_picthclass(symbol)
            a_pos = (r_pitchclass + pos) % self.pitchclass.classes
            positions.append(cyclic_difference(a_pos, n_pos, self.pitchclass.classes))
        return tuple(positions)

    def is_keyname(self, value: object) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.keynames

    def ensure_valid_keyname(self, keyname: str) -> None:
        if not self.is_keyname(keyname):
            raise ValueError
