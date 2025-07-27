import typing as t
from dataclasses import dataclass
from functools import cached_property
from itertools import chain

from aulos._core.pitch import PitchSchema
from aulos._core.schema import Schema
from aulos._core.utils import Intervals, Positions


def create_upper_sequences(
    symbols_pitchclass: tuple[str, ...],
    symbols_accidental: tuple[str, ...],
    standard_positions: Positions,
) -> list[list[str | None]]:
    accidentals = symbols_accidental[get_accidental_count(symbols_accidental) :]
    return [
        create_natural_sequence(symbols_pitchclass, (acc,), standard_positions)[0][-i:]
        + create_natural_sequence(symbols_pitchclass, (acc,), standard_positions)[0][:-i]
        for i, acc in enumerate(accidentals, start=1)
    ]


def create_lower_sequences(
    symbols_pitchclass: tuple[str, ...],
    symbols_accidental: tuple[str, ...],
    standard_positions: Positions,
) -> list[list[str | None]]:
    accidentals = symbols_accidental[: get_accidental_count(symbols_accidental)]
    return [
        create_natural_sequence(symbols_pitchclass, (acc,), standard_positions)[0][i:]
        + create_natural_sequence(symbols_pitchclass, (acc,), standard_positions)[0][:i]
        for i, acc in enumerate(reversed(accidentals), start=1)
    ]


def create_natural_sequence(
    symbols_pitchclass: tuple[str, ...],
    symbols_accidental: tuple[str, ...],
    standard_positions: Positions,
) -> list[list[str | None]]:
    return [
        [
            get_formated_pitchname(
                symbols_pitchclass[standard_positions.index(pos)],
                acc,
            )
            if pos in standard_positions
            else None
            for pos in range(standard_positions.limit)
        ]
        for acc in symbols_accidental
    ]


def get_formated_pitchname(
    symbols_pitchclass: str,
    symbols_accidental: str,
) -> str:
    if symbols_accidental.find("<P>") >= 0:
        return symbols_accidental.replace("<P>", symbols_pitchclass.upper())
    if symbols_accidental.find("<p>") >= 0:
        return symbols_accidental.replace("<p>", symbols_pitchclass.lower())
    return f"{symbols_pitchclass}{symbols_accidental}"


def get_accidental_count(symbols_accidental: tuple[str, ...]) -> int:
    return len(symbols_accidental) // 2


@dataclass(init=False, frozen=True, slots=True)
class PitchClassSchema(Schema):
    classes: int
    accidental: int
    symbols_pitchclass: tuple[str, ...]
    symbols_accidental: tuple[str, ...]
    standard_intervals: Intervals
    standard_positions: Positions
    name2class: dict[str, int]
    class2name: dict[int, tuple[str | None, ...]]
    pitch: PitchSchema

    def __init__(
        self,
        /,
        intervals: tuple[int, ...],
        symbols_pitchclass: tuple[str, ...],
        symbols_accidental: tuple[str, ...],
        pitch: PitchSchema,
    ) -> None:
        super(Schema, self).__init__()

        standard_intervals = Intervals(intervals)
        standard_positions = standard_intervals.to_positions()
        classes = standard_positions.limit
        accidental = get_accidental_count(symbols_accidental)

        accidental_natural_sequence = create_natural_sequence(
            symbols_pitchclass,
            ("",),
            standard_positions,
        )
        accidental_upper_sequences = create_upper_sequences(
            symbols_pitchclass,
            symbols_accidental,
            standard_positions,
        )
        accidental_lower_sequences = reversed(
            create_lower_sequences(
                symbols_pitchclass,
                symbols_accidental,
                standard_positions,
            )
        )
        accidental_sequences = tuple(
            zip(
                *accidental_lower_sequences,
                *accidental_natural_sequence,
                *accidental_upper_sequences,
                strict=False,
            ),
        )
        name2class = [
            [(name, index) for name in names if name is not None] for index, names in enumerate(accidental_sequences)
        ]
        class2name = [(index, name) for index, name in enumerate(accidental_sequences)]

        object.__setattr__(self, "classes", classes)
        object.__setattr__(self, "accidental", accidental)
        object.__setattr__(self, "symbols_pitchclass", symbols_pitchclass)
        object.__setattr__(self, "symbols_accidental", symbols_accidental)
        object.__setattr__(self, "standard_intervals", standard_intervals)
        object.__setattr__(self, "standard_positions", standard_positions)
        object.__setattr__(self, "name2class", dict(chain.from_iterable(name2class)))
        object.__setattr__(self, "class2name", dict(class2name))
        object.__setattr__(self, "pitch", pitch)

    def validate(self) -> None:
        pass

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

    def get_intervals(self, pitchname: str) -> Intervals:
        positions = self.get_positions(pitchname)
        return positions.to_intervals()

    def get_positions(self, pitchname: str) -> Positions:
        self.ensure_valid_pitchname(pitchname)
        pitchclass = self.convert_pitchname_to_picthclass(pitchname)
        accidental = self.get_accidental(pitchname)
        positions = [
            pos
            for pos in range(self.classes)
            if self.convert_pitchclass_to_pitchname((pos + pitchclass) % self.classes, accidental) is not None
        ]
        return Positions(positions, limit=self.classes)

    def get_accidental(self, pitchname: str) -> int:
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
        accidental = self.get_accidental(pitchname)
        pitchclass = self.convert_pitchname_to_picthclass(pitchname)
        pitchclass = (pitchclass - accidental) % self.classes
        symbol = self.convert_pitchclass_to_pitchname(pitchclass, 0)
        if symbol is None:
            msg = "unreachable error"
            raise RuntimeError(msg)
        return symbol

    def is_symbol(self, value: object) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.symbols_pitchclass

    def is_pitchname(self, value: object) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.pitchnames

    def is_pitchclass(self, value: object) -> t.TypeGuard[int]:
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


@dataclass(init=False, frozen=True, slots=True)
class PitchClassCollectionSchema(Schema):
    def __init__(self) -> None:
        super(Schema, self).__init__()

    def validate(self) -> None:
        pass
