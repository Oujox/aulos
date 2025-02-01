import typing as t
from dataclasses import dataclass, field
from functools import cached_property
from itertools import accumulate, chain

from aulos._core import Schema
from aulos._errors import ValidationError


@dataclass(frozen=True, slots=True)
class PitchClassSchema(Schema):
    intervals: tuple[int, ...]
    symbols_pitchclass: tuple[str, ...]
    symbols_accidental: tuple[str, ...]

    cardinality: int = field(init=False)
    accidental: int = field(init=False)
    positions: tuple[int, ...] = field(init=False)
    name2class: dict[str, int] = field(init=False)
    class2name: dict[int, tuple[str | None, ...]] = field(init=False)

    def __post_init__(self) -> None:
        self.validate()
        self.initialize()

    def validate(self) -> None:
        # [check] intervals
        if not len(self.intervals) > 0:
            msg = ""
            raise ValidationError(msg)
        if not all(v >= 0 for v in self.intervals):
            msg = ""
            raise ValidationError(msg)

        # [check] symbols_pitchclass
        if not len(self.symbols_pitchclass) > 0:
            msg = ""
            raise ValidationError(msg)

        # [check] symbols_accidental
        if not len(self.symbols_accidental) > 0:
            msg = ""
            raise ValidationError(msg)
        if len(self.symbols_accidental) % 2 != 0:
            msg = ""
            raise ValidationError(msg)

        # [cross-field check]
        if len(self.intervals) != len(self.symbols_pitchclass):
            msg = ""
            raise ValidationError(msg)

    def initialize(self) -> None:
        cardinality = sum(self.intervals)
        positions = tuple(accumulate((0,) + self.intervals[:-1]))

        accidental = len(self.symbols_accidental) // 2
        upper_accidentals = self.symbols_accidental[accidental:]
        lower_accidentals = reversed(self.symbols_accidental[:accidental])

        def create_upper_sequences() -> list[list[str | None]]:
            sequences = []
            for i, acc in enumerate(upper_accidentals, start=1):
                sequence = create_symbol_sequence(suffix=acc)
                for _ in range(i):
                    sequence.insert(0, sequence.pop())
                sequences.append(sequence)
            return sequences

        def create_lower_sequences() -> list[list[str | None]]:
            sequences = []
            for i, acc in enumerate(lower_accidentals, start=1):
                sequence = create_symbol_sequence(suffix=acc)
                for _ in range(i):
                    sequence.append(sequence.pop(0))
                sequences.append(sequence)
            return sequences

        def create_symbol_sequence(
            *,
            prefix: str = "",
            suffix: str = "",
        ) -> list[str | None]:
            sequence: list[str | None] = []
            for deg in range(cardinality):
                if deg in positions:
                    index = positions.index(deg)
                    sequence.append(prefix + self.symbols_pitchclass[index] + suffix)
                else:
                    sequence.append(None)
            return sequence

        no_accidental_sequence = create_symbol_sequence()
        accidental_upper_sequences = create_upper_sequences()
        accidental_lower_sequences = reversed(create_lower_sequences())
        accidental_sequences = tuple(
            zip(
                *accidental_lower_sequences,
                no_accidental_sequence,
                *accidental_upper_sequences,
                strict=False,
            ),
        )
        name2class = [
            [(name, index) for name in names if name is not None] for index, names in enumerate(accidental_sequences)
        ]
        class2name = [(index, name) for index, name in enumerate(accidental_sequences)]

        object.__setattr__(self, "cardinality", cardinality)
        object.__setattr__(self, "accidental", accidental)
        object.__setattr__(self, "positions", positions)
        object.__setattr__(self, "name2class", dict(chain.from_iterable(name2class)))
        object.__setattr__(self, "class2name", dict(class2name))

    @cached_property
    def pitchnames(self) -> tuple[str, ...]:
        return tuple(self.name2class.keys())

    @cached_property
    def pitchclasses(self) -> tuple[int, ...]:
        return tuple(self.class2name.keys())

    # unstable
    def find_pitchname(self, value: str) -> str | None:
        finded = sorted(
            [pitchname for pitchname in self.pitchnames if value.find(pitchname) == 0],
            key=len,
            reverse=True,
        )
        return ([*finded, None])[0]

    def count_accidental(self, pitchname: str) -> int:
        self.ensure_valid_pitchname(pitchname)
        pitchclass = self.convert_pitchname_to_picthclass(pitchname)
        pitchnames = self.convert_pitchclass_to_pitchnames(pitchclass)
        return pitchnames.index(pitchname) - self.accidental

    def convert_pitchclass_to_pitchname(
        self,
        pitchclass: int,
        accidental: int,
    ) -> str | None:
        self.ensure_valid_pitchclass(pitchclass)
        self.ensure_valid_accidental(accidental)
        return self.class2name[pitchclass][self.accidental + accidental]

    def convert_pitchclass_to_pitchnames(
        self,
        pitchclass: int,
    ) -> tuple[str | None, ...]:
        self.ensure_valid_pitchclass(pitchclass)
        return self.class2name[pitchclass]

    def convert_pitchname_to_picthclass(self, pitchname: str) -> int:
        self.ensure_valid_pitchname(pitchname)
        return self.name2class[pitchname]

    def convert_pitchclass_to_symbol(self, pitchclass: int) -> str | None:
        self.ensure_valid_pitchclass(pitchclass)
        return self.convert_pitchclass_to_pitchnames(pitchclass)[self.accidental]

    def convert_pitchname_to_symbol(self, pitchname: str) -> str:
        self.ensure_valid_pitchname(pitchname)
        accidental = self.count_accidental(pitchname)
        pitchclass = self.convert_pitchname_to_picthclass(pitchname)
        pitchclass = (pitchclass - accidental) % self.cardinality
        symbol = self.convert_pitchclass_to_pitchname(pitchclass, 0)
        if symbol is None:
            msg = "unreachable error"
            raise RuntimeError(msg)
        return symbol

    def is_symbol(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.symbols_pitchclass

    def is_pitchname(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.pitchnames

    def is_pitchclass(self, value: t.Any) -> t.TypeGuard[int]:
        return isinstance(value, int) and value in self.pitchclasses

    def ensure_valid_pitchname(self, pitchname: str) -> None:
        if not self.is_pitchname(pitchname):
            msg = f"Invalid pitchname '{pitchname}'. Pitchname must be a valid musical note name {self.pitchnames[:3]}."
            raise ValueError(
                msg,
            )

    def ensure_valid_pitchclass(self, pitchclass: int) -> None:
        if not self.is_pitchclass(pitchclass):
            msg = (
                f"Invalid pitchclass '{pitchclass}'."
                f"Pitchclass must be an integer between {min(self.pitchclasses)} and"
                f"{max(self.pitchclasses)} inclusive."
            )
            raise ValueError(
                msg,
            )

    def ensure_valid_accidental(self, accidental: int) -> None:
        if not abs(accidental) <= self.accidental:
            msg = (
                f"Invalid accidental '{accidental}'. "
                f"Accidental must be within the range -{self.accidental} to +{self.accidental}."
            )
            raise ValueError(
                msg,
            )
