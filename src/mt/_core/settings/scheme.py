import typing as t
from dataclasses import dataclass, field
from functools import cached_property
from itertools import accumulate, chain

from ..utils import diff


@dataclass(frozen=True)
class AccidentalSetting:
    limit: int
    upper_symbol: str
    lower_symbol: str


@dataclass(frozen=True)
class SchemeSetting:
    semitone: int
    symbols: list[str]
    intervals: list[int]
    accidental: AccidentalSetting

    positions: tuple[int] = field(init=False)
    name2class: dict[str, int] = field(init=False)
    class2name: dict[int, tuple[str]] = field(init=False)

    def __post_init__(self):
        object.__setattr__(
            self, "positions", tuple(accumulate([0] + self.intervals[:-1]))
        )

        accidental_no_sequence = create_symbol_sequence(self)
        accidental_upper_sequences = create_upper_sequences(self)
        accidental_lower_sequences = create_lower_sequences(self)
        accidental_lower_sequences.reverse()
        accidental_sequences = tuple(
            zip(
                *accidental_lower_sequences,
                accidental_no_sequence,
                *accidental_upper_sequences,
            )
        )
        name2class = [
            [(name, index) for name in names if name is not None]
            for index, names in enumerate(accidental_sequences)
        ]
        class2name = [(index, name) for index, name in enumerate(accidental_sequences)]

        object.__setattr__(self, "name2class", dict(chain.from_iterable(name2class)))
        object.__setattr__(self, "class2name", dict(class2name))

    @cached_property
    def pitchnames(self) -> tuple[str]:
        return tuple(self.name2class.keys())

    @cached_property
    def pitchclasses(self) -> tuple[int]:
        return tuple(self.class2name.keys())

    def generate_accidentals(self, pitchname: str) -> tuple[int]:
        if not self.is_pitchname(pitchname):
            raise ValueError(f"Invalid notename: '{pitchname}'.")

        positions = []
        r_symbol = self.convert_pitchname_to_symbol(pitchname)
        r_pitchclass = self.convert_pitchname_to_picthclass(pitchname)

        idx = self.symbols.index(r_symbol)
        symbols = self.symbols[idx:] + self.symbols[:idx]

        for pos, symbol in zip(self.positions, symbols):
            n_pos = self.convert_pitchname_to_picthclass(symbol)
            a_pos = (r_pitchclass + pos) % self.semitone
            positions.append(diff(a_pos, n_pos, self.semitone))
        return positions

    def count_accidental(self, pitchname: str) -> t.Optional[int]:
        if self.is_pitchname(pitchname):
            count_acc_upper = pitchname.count(self.accidental.upper_symbol)
            count_acc_lower = pitchname.count(self.accidental.lower_symbol)
            return count_acc_upper - count_acc_lower
        return None

    def convert_pitchclass_to_symbol(self, pitchclass: int) -> t.Optional[str]:
        if not self.is_pitchclass(pitchclass):
            raise ValueError(f"Invalid pitchclass: '{pitchclass}'.")
        return self.convert_pitchclass_to_pitchnames(pitchclass)[self.accidental.limit]

    def convert_pitchclass_to_pitchname(
        self, pitchclass: int, accidental: int
    ) -> t.Optional[str]:
        if not self.is_pitchclass(pitchclass):
            raise ValueError(f"Invalid pitchclass: '{pitchclass}'.")
        return self.convert_pitchclass_to_pitchnames(pitchclass)[
            self.accidental.limit + accidental
        ]

    def convert_pitchclass_to_pitchnames(
        self, pitchclass: int
    ) -> tuple[t.Optional[str]]:
        if not self.is_pitchclass(pitchclass):
            raise ValueError(f"Invalid pitchclass: '{pitchclass}'.")
        return self.class2name[pitchclass]

    def convert_pitchname_to_picthclass(self, pitchname: str) -> int:
        if not self.is_pitchname(pitchname):
            raise ValueError(f"Invalid notename: '{pitchname}'.")
        return self.name2class[pitchname]

    def convert_pitchname_to_symbol(self, pitchname: str):
        if not self.is_pitchname(pitchname):
            raise ValueError(f"Invalid notename: '{pitchname}'.")
        return pitchname.replace(self.accidental.upper_symbol, "").replace(
            self.accidental.lower_symbol, ""
        )

    def is_symbol(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.symbols

    def is_pitchname(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.pitchnames

    def is_pitchclass(self, value: t.Any) -> t.TypeGuard[int]:
        return isinstance(value, int) and 0 <= value < self.semitone


def create_upper_sequences(scheme: SchemeSetting) -> list[list[str]]:
    sequences = []
    for i in range(1, scheme.accidental.limit + 1):
        sequence = create_symbol_sequence(
            scheme, suffix=scheme.accidental.upper_symbol * i
        )
        for _ in range(i):
            sequence.insert(0, sequence.pop())
        sequences.append(sequence)
    return sequences


def create_lower_sequences(scheme: SchemeSetting) -> list[list[str]]:
    sequences = []
    for i in range(1, scheme.accidental.limit + 1):
        sequence = create_symbol_sequence(
            scheme, suffix=scheme.accidental.lower_symbol * i
        )
        for _ in range(i):
            sequence.append(sequence.pop(0))
        sequences.append(sequence)
    return sequences


def create_symbol_sequence(
    scheme: SchemeSetting, *, prefix: str = "", suffix: str = ""
) -> list[str]:
    sequence = []
    for deg in range(scheme.semitone):
        if deg in scheme.positions:
            index = scheme.positions.index(deg)
            sequence.append(prefix + scheme.symbols[index] + suffix)
        else:
            sequence.append(None)
    return sequence
