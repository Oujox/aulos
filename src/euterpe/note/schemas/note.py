import typing as t
from dataclasses import dataclass, field
from functools import cached_property
from itertools import chain

from ..._core import Schema
from .pitchclass import PitchClassSchema


@dataclass(frozen=True, slots=True)
class NoteSchema(Schema):

    symbols_notenumber: tuple[int, ...]
    symbols_octave: tuple[str, ...]
    reference_notenumber: int
    reference_octave: int
    pitchclass: PitchClassSchema

    name2number: dict[str, int] = field(init=False)
    number2name: dict[int, tuple[str | None]] = field(init=False)

    def __post_init__(self) -> None:
        self.validate()
        self.initialize()

    def validate(self) -> None:
        # [check] symbols_notenumber
        if not len(self.symbols_notenumber) > 0:
            raise Exception()
        if not all(0 <= v for v in self.symbols_notenumber):
            raise Exception()

        # [check] symbols_octave
        if not len(self.symbols_octave) > 0:
            raise Exception()
        if not all(
            bool(v.find("<N>")) or bool(v.find("<n>")) for v in self.symbols_octave
        ):
            raise Exception()

        # [check] reference_notenumber
        if not self.reference_notenumber in self.symbols_notenumber:
            raise Exception()

        # [check] reference_octave
        if not self.reference_octave in range(len(self.symbols_octave)):
            raise Exception()

    def initialize(self) -> None:
        accidental = len(self.pitchclass.symbols_accidental) // 2
        upper_accidentals = self.pitchclass.symbols_accidental[accidental:]
        lower_accidentals = self.pitchclass.symbols_accidental[:accidental]
        lower_accidentals = reversed(lower_accidentals)

        def create_upper_sequences():
            sequences: list[list[str]] = []
            for i, acc in enumerate(upper_accidentals, start=1):
                sequence = create_symbol_sequence(suffix=acc)
                for _ in range(i):
                    sequence.insert(0, sequence.pop())
                sequences.append(sequence)
            return sequences

        def create_lower_sequences():
            sequences: list[list[str]] = []
            for i, acc in enumerate(lower_accidentals, start=1):
                sequence = create_symbol_sequence(suffix=acc)
                for _ in range(i):
                    sequence.append(sequence.pop(0))
                sequences.append(sequence)
            return sequences

        def create_symbol_sequence(*, prefix: str = "", suffix: str = "") -> list[str]:
            sequence = []
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
        
        def convert_pitchname_to_notename(pitchname: str, symbol_octave: str) -> str:
            # <N>
            if symbol_octave.find("<N>") >= 0:
                return symbol_octave.replace("<N>", pitchname, 1)
            # <n>
            elif symbol_octave.find("<n>") >= 0:
                return symbol_octave.replace("<n>", pitchname, 1)
            else:
                return symbol_octave + pitchname
        
        no_accidental_sequence = create_symbol_sequence()
        accidental_upper_sequences = create_upper_sequences()
        accidental_lower_sequences = create_lower_sequences()
        accidental_lower_sequences = reversed(accidental_lower_sequences)
        accidental_sequences = tuple(
            zip(
                *accidental_lower_sequences,
                no_accidental_sequence,
                *accidental_upper_sequences,
            )
        )

        # adjust notenumber
        ref_pitchname = self.pitchclass.symbols_pitchclass[0]
        ref_octave_notename = convert_pitchname_to_notename(
            ref_pitchname, self.symbols_octave[self.reference_octave]
        )
        adjust_notenumber = (
            self.reference_notenumber - no_accidental_sequence.index(ref_octave_notename)
        )

        name2number = dict(chain.from_iterable([
            [(name, index + adjust_notenumber) for name in names if name is not None]
            for index, names in enumerate(accidental_sequences)
            if index + adjust_notenumber in self.symbols_notenumber
        ]))
        number2name = dict([
            (index + adjust_notenumber, name)
            for index, name in enumerate(accidental_sequences)
            if index + adjust_notenumber in self.symbols_notenumber
        ])

        object.__setattr__(self, "name2number", name2number)
        object.__setattr__(self, "number2name", number2name)

    @cached_property
    def notenames(self) -> tuple[str, ...]:
        return tuple(self.name2number.keys())

    @cached_property
    def notenumbers(self) -> tuple[int, ...]:
        return tuple(self.number2name.keys())

    def count_accidental(self, notename: str) -> int:
        self.ensure_valid_notename(notename)
        notenumber = self.convert_notename_to_notenumber(notename)
        notenames = self.convert_notenumber_to_notenames(notenumber)
        return notenames.index(notename) - self.pitchclass.accidental

    def convert_notenumber_to_notename(
        self, notenumber: int, accidental: int
    ) -> str | None:
        self.ensure_valid_notenumber(notenumber)
        return self.number2name[notenumber][self.pitchclass.accidental + accidental]

    def convert_notenumber_to_notenames(
        self, notenumber: int
    ) -> tuple[str | None, ...]:
        self.ensure_valid_notenumber(notenumber)
        return self.number2name[notenumber]

    def convert_notename_to_notenumber(self, notename: str) -> int:
        self.ensure_valid_notename(notename)
        return self.name2number[notename]

    # [unstable]
    def convert_notenumber_to_pitchclass(self, notenumber: int) -> int:
        self.ensure_valid_notenumber(notenumber)
        return notenumber % self.pitchclass.cardinality

    # [unstable]
    def convert_pitchclass_to_notenumber(self, pitchclass: int, octave: int) -> int:
        self.pitchclass.ensure_valid_pitchclass(pitchclass)
        return pitchclass + (self.pitchclass.cardinality * octave)

    # [unstable]
    def convert_notename_to_pitchname(self, notename: str) -> str:
        self.ensure_valid_notename(notename)
        accidental = self.count_accidental(notename)
        notenumber = self.convert_notename_to_notenumber(notename)
        pitchclass = self.convert_notenumber_to_pitchclass(notenumber)
        pitchname = self.pitchclass.convert_pitchclass_to_pitchname(
            pitchclass, accidental
        )
        if pitchname is None:
            raise RuntimeError("unreachable error")
        return pitchname

    # [unstable]
    def convert_pitchname_to_notename(self, pitchname: str, octave: int) -> str:
        self.pitchclass.ensure_valid_pitchname(pitchname)
        accidental = self.pitchclass.count_accidental(pitchname)
        pitchclass = self.pitchclass.convert_pitchname_to_picthclass(pitchname)
        notenumber = self.convert_pitchclass_to_notenumber(pitchclass, octave)
        notename = self.convert_notenumber_to_notename(notenumber, accidental)
        if notename is None:
            raise RuntimeError("unreachable error")
        return notename

    def is_notename(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.notenames

    def is_notenumber(self, value: t.Any) -> t.TypeGuard[int]:
        return isinstance(value, int) and value in self.notenumbers

    def ensure_valid_notename(self, notename: str) -> None:
        if not self.is_notename(notename):
            raise ValueError(
                f"Invalid notename '{notename}'. "
                f"Notename must be a valid musical note name {self.notenames[:3]}."
            )

    def ensure_valid_notenumber(self, notenumber: int) -> None:
        if not self.is_notenumber(notenumber):
            raise ValueError(
                f"Invalid pitchclass '{notenumber}'."
                f"Notenumber must be an integer between {min(self.notenumbers)} and {max(self.notenumbers)} inclusive."
            )
