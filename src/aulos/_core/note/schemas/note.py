import typing as t
from dataclasses import dataclass, field
from functools import cached_property
from itertools import chain

from aulos._core.schema import Schema
from aulos._errors import ValidationError

from .pitchclass import PitchClassSchema


def convert_pitchname_to_notename(pitchname: str, symbol_octave: str) -> str:
    # <N>
    if symbol_octave.find("<N>") >= 0:
        return symbol_octave.replace("<N>", pitchname, 1)
    # <n>
    if symbol_octave.find("<n>") >= 0:
        return symbol_octave.replace("<n>", pitchname, 1)
    return symbol_octave + pitchname


@dataclass(frozen=True, slots=True)
class NoteSchema(Schema):
    symbols_notenumber: tuple[int, ...]
    symbols_octave: tuple[str, ...]
    reference_notenumber: int
    pitchclass: PitchClassSchema

    name2number: dict[str, int] = field(init=False)
    number2name: dict[int, tuple[str | None]] = field(init=False)

    def __post_init__(self) -> None:
        self.validate()
        self.initialize()

    def validate(self) -> None:
        # [check] symbols_notenumber
        if not len(self.symbols_notenumber) > 0:
            msg = ""
            raise ValidationError(msg)
        if not all(v >= 0 for v in self.symbols_notenumber):
            msg = ""
            raise ValidationError(msg)

        # [check] symbols_octave
        if not len(self.symbols_octave) > 0:
            msg = ""
            raise ValidationError(msg)
        if not all(bool(v.find("<N>")) or bool(v.find("<n>")) for v in self.symbols_octave):
            msg = ""
            raise ValidationError(msg)

        # [check] reference_notenumber
        if self.reference_notenumber not in self.symbols_notenumber:
            msg = ""
            raise ValidationError(msg)

    def initialize(self) -> None:
        accidental = len(self.pitchclass.symbols_accidental) // 2
        upper_accidentals = self.pitchclass.symbols_accidental[accidental:]
        lower_accidentals = reversed(self.pitchclass.symbols_accidental[:accidental])

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
            for symbol_octave in self.symbols_octave:
                for deg in range(self.pitchclass.cardinality):
                    if deg in self.pitchclass.positions:
                        index = self.pitchclass.positions.index(deg)
                        pitchname = prefix + self.pitchclass.symbols_pitchclass[index] + suffix
                        notename = convert_pitchname_to_notename(
                            pitchname,
                            symbol_octave,
                        )
                        sequence.append(notename)
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

        name2number = dict(
            chain.from_iterable(
                [
                    [(name, index) for name in names if name is not None]
                    for index, names in enumerate(accidental_sequences)
                    if index in self.symbols_notenumber
                ],
            ),
        )
        number2name = {
            index: name for index, name in enumerate(accidental_sequences) if index in self.symbols_notenumber
        }

        object.__setattr__(self, "name2number", name2number)
        object.__setattr__(self, "number2name", number2name)

    @cached_property
    def notenames(self) -> tuple[str, ...]:
        return tuple(self.name2number.keys())

    @cached_property
    def notenumbers(self) -> tuple[int, ...]:
        return tuple(self.number2name.keys())

    def find_nearest_notename(
        self, reference_notename: str, target_pitchname: str, direction: t.Literal["up", "down"] = "down"
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
        return notenumber // self.pitchclass.cardinality

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
        return notenumber % self.pitchclass.cardinality

    def convert_pitchclass_to_notenumber(self, pitchclass: int, octave: int) -> int:
        self.pitchclass.ensure_valid_pitchclass(pitchclass)
        return pitchclass + (self.pitchclass.cardinality * octave)

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
