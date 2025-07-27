import typing as t
from dataclasses import dataclass
from functools import cached_property
from itertools import chain

from aulos._core.pitchclass import PitchClassSchema
from aulos._core.schema import Schema
from aulos._core.utils import Positions


def create_upper_sequences(
    symbols_pitchclass: tuple[str, ...],
    symbols_accidental: tuple[str, ...],
    symbols_octave: tuple[str, ...],
    standard_positions: Positions,
) -> list[list[str | None]]:
    accidentals = symbols_accidental[get_accidental_count(symbols_accidental) :]
    return [
        create_natural_sequence(symbols_pitchclass, (acc,), symbols_octave, standard_positions)[0][-i:]
        + create_natural_sequence(symbols_pitchclass, (acc,), symbols_octave, standard_positions)[0][:-i]
        for i, acc in enumerate(accidentals, start=1)
    ]


def create_lower_sequences(
    symbols_pitchclass: tuple[str, ...],
    symbols_accidental: tuple[str, ...],
    symbols_octave: tuple[str, ...],
    standard_positions: Positions,
) -> list[list[str | None]]:
    accidentals = symbols_accidental[: get_accidental_count(symbols_accidental)]
    return [
        create_natural_sequence(symbols_pitchclass, (acc,), symbols_octave, standard_positions)[0][i:]
        + create_natural_sequence(symbols_pitchclass, (acc,), symbols_octave, standard_positions)[0][:i]
        for i, acc in enumerate(reversed(accidentals), start=1)
    ]


def create_natural_sequence(
    symbols_pitchclass: tuple[str, ...],
    symbols_accidental: tuple[str, ...],
    symbols_octave: tuple[str, ...],
    standard_positions: Positions,
) -> list[list[str | None]]:
    return [
        [
            get_formated_notename(
                get_formated_pitchname(symbols_pitchclass[standard_positions.index(pos)], symbol_accidental),
                symbol_octave,
            )
            if pos in standard_positions
            else None
            for symbol_octave in symbols_octave
            for pos in range(standard_positions.limit)
        ]
        for symbol_accidental in symbols_accidental
    ]


def get_formated_pitchname(
    symbols_pitchclass: str,
    symbols_accidental: str,
) -> str:
    if symbols_accidental.find("<P>") >= 0:
        return symbols_accidental.replace("<P>", symbols_pitchclass)
    if symbols_accidental.find("<p>") >= 0:
        return symbols_accidental.replace("<p>", symbols_pitchclass)
    return f"{symbols_pitchclass}{symbols_accidental}"


def get_formated_notename(pitchname: str, symbol_octave: str) -> str:
    if symbol_octave.find("<N>") >= 0:
        return symbol_octave.replace("<N>", pitchname)
    if symbol_octave.find("<n>") >= 0:
        return symbol_octave.replace("<n>", pitchname)
    return f"{pitchname}{symbol_octave}"


def get_accidental_count(symbols_accidental: tuple[str, ...]) -> int:
    return len(symbols_accidental) // 2


@dataclass(init=False, frozen=True, slots=True)
class NoteSchema(Schema):
    symbols_notenumber: tuple[int, ...]
    symbols_octave: tuple[str, ...]
    name2number: dict[str, int]
    number2name: dict[int, tuple[str | None]]
    pitchclass: PitchClassSchema

    def __init__(
        self,
        /,
        symbols_notenumber: tuple[int, ...],
        symbols_octave: tuple[str, ...],
        pitchclass: PitchClassSchema,
    ) -> None:
        super(Schema, self).__init__()

        accidental_natural_sequences = create_natural_sequence(
            pitchclass.symbols_pitchclass,
            ("",),
            symbols_octave,
            pitchclass.standard_positions,
        )
        accidental_upper_sequences = create_upper_sequences(
            pitchclass.symbols_pitchclass,
            pitchclass.symbols_accidental,
            symbols_octave,
            pitchclass.standard_positions,
        )
        accidental_lower_sequences = reversed(
            create_lower_sequences(
                pitchclass.symbols_pitchclass,
                pitchclass.symbols_accidental,
                symbols_octave,
                pitchclass.standard_positions,
            ),
        )
        accidental_sequences = tuple(
            zip(
                *accidental_lower_sequences,
                *accidental_natural_sequences,
                *accidental_upper_sequences,
                strict=False,
            ),
        )

        name2number = [
            [(name, index) for name in names if name is not None]
            for index, names in enumerate(accidental_sequences)
            if index in symbols_notenumber
        ]
        number2name = [(index, name) for index, name in enumerate(accidental_sequences) if index in symbols_notenumber]

        object.__setattr__(self, "symbols_notenumber", symbols_notenumber)
        object.__setattr__(self, "symbols_octave", symbols_octave)
        object.__setattr__(self, "name2number", dict(chain.from_iterable(name2number)))
        object.__setattr__(self, "number2name", dict(number2name))
        object.__setattr__(self, "pitchclass", pitchclass)

    def validate(self) -> None:
        pass

    @cached_property
    def notenames(self) -> tuple[str, ...]:
        return tuple(self.name2number.keys())

    @cached_property
    def notenumbers(self) -> tuple[int, ...]:
        return tuple(self.number2name.keys())

    def find_nearest_notename(
        self, reference_notename: str, target_pitchname: str, direction: t.Literal["up", "down"] = "down",
    ) -> str | None:
        self.ensure_valid_notename(reference_notename)
        self.pitchclass.ensure_valid_pitchname(target_pitchname)

        if direction == "up":
            reference_notenumber = self.convert_notename_to_notenumber(reference_notename)
            target_accidental = self.pitchclass.get_accidental(target_pitchname)
            for notenumber in sorted(self.number2name.keys()):
                if notenumber > reference_notenumber:
                    candidate_notename = self.convert_notenumber_to_notename(notenumber, target_accidental)
                    if (
                        candidate_notename is not None
                        and self.convert_notename_to_pitchname(candidate_notename) == target_pitchname
                    ):
                        return candidate_notename
            return None

        if direction == "down":
            reference_notenumber = self.convert_notename_to_notenumber(reference_notename)
            target_accidental = self.pitchclass.get_accidental(target_pitchname)
            for notenumber in sorted(self.number2name.keys(), reverse=True):
                if notenumber < reference_notenumber:
                    candidate_notename = self.convert_notenumber_to_notename(notenumber, target_accidental)
                    if (
                        candidate_notename is not None
                        and self.convert_notename_to_pitchname(candidate_notename) == target_pitchname
                    ):
                        return candidate_notename
            return None
        return None

    def get_accidental(self, notename: str) -> int:
        self.ensure_valid_notename(notename)
        notenumber = self.convert_notename_to_notenumber(notename)
        notenames = self.convert_notenumber_to_notenames(notenumber)
        return notenames.index(notename) - self.pitchclass.accidental

    def get_octave(self, notenumber: int) -> int:
        self.ensure_valid_notenumber(notenumber)
        return notenumber // self.pitchclass.classes

    def convert_notenumber_to_notename(
        self,
        notenumber: int,
        accidental: int,
    ) -> str | None:
        self.ensure_valid_notenumber(notenumber)
        return self.number2name[notenumber][self.pitchclass.accidental + accidental]

    def convert_notenumber_to_notenames(
        self,
        notenumber: int,
    ) -> tuple[str | None, ...]:
        self.ensure_valid_notenumber(notenumber)
        return self.number2name[notenumber]

    def convert_notename_to_notenumber(self, notename: str) -> int:
        self.ensure_valid_notename(notename)
        return self.name2number[notename]

    def convert_notenumber_to_pitchclass(self, notenumber: int) -> int:
        self.ensure_valid_notenumber(notenumber)
        return notenumber % self.pitchclass.classes

    def convert_pitchclass_to_notenumber(self, pitchclass: int, octave: int) -> int:
        self.pitchclass.ensure_valid_pitchclass(pitchclass)
        return pitchclass + (self.pitchclass.classes * octave)

    def convert_notename_to_pitchname(self, notename: str) -> str:
        self.ensure_valid_notename(notename)
        accidental = self.get_accidental(notename)
        notenumber = self.convert_notename_to_notenumber(notename)
        pitchclass = self.convert_notenumber_to_pitchclass(notenumber)
        pitchname = self.pitchclass.convert_pitchclass_to_pitchname(
            pitchclass,
            accidental,
        )
        if pitchname is None:
            msg = "unreachable error"
            raise RuntimeError(msg)
        return pitchname

    def convert_pitchname_to_notename(self, pitchname: str, octave: int) -> str:
        self.pitchclass.ensure_valid_pitchname(pitchname)
        accidental = self.pitchclass.get_accidental(pitchname)
        pitchclass = self.pitchclass.convert_pitchname_to_picthclass(pitchname)
        notenumber = self.convert_pitchclass_to_notenumber(pitchclass, octave)
        notename = self.convert_notenumber_to_notename(notenumber, accidental)
        if notename is None:
            msg = "unreachable error"
            raise RuntimeError(msg)
        return notename

    def is_notename(self, value: object) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.notenames

    def is_notenumber(self, value: object) -> t.TypeGuard[int]:
        return isinstance(value, int) and value in self.notenumbers

    def ensure_valid_notename(self, notename: str) -> None:
        if not self.is_notename(notename):
            msg = f"Invalid notename '{notename}'. Notename must be a valid musical note name {self.notenames[:3]}."
            raise ValueError(
                msg,
            )

    def ensure_valid_notenumber(self, notenumber: int) -> None:
        if not self.is_notenumber(notenumber):
            msg = (
                f"Invalid pitchclass '{notenumber}'."
                f"Notenumber must be an integer between {min(self.notenumbers)} and {max(self.notenumbers)} inclusive."
            )
            raise ValueError(
                msg,
            )
