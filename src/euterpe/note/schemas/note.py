import typing as t
from dataclasses import dataclass, field
from functools import cached_property

from ..._core import Schema
from .pitchclass import PitchClassSchema


@dataclass(frozen=True, slots=True)
class NoteSchema(Schema):

    symbols_notenumber: tuple[int, ...]
    symbols_octave: tuple[str, ...]
    reference_notenumber: int
    reference_octave: int
    pitchclass: PitchClassSchema

    adjust_notenumber: int = field(init=False)
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

        def convert_pitchclass_to_notenumber(pitchclass: int, octave: int) -> int:
            return pitchclass + (octave * self.pitchclass.cardinality)

        def convert_pitchnames_to_notenames(
            pitchnames: tuple[str | None, ...], symbol_octave: str
        ) -> tuple[str | None, ...]:
            return tuple(
                (
                    convert_pitchname_to_notename(pitchname, symbol_octave)
                    if pitchname is not None
                    else None
                )
                for pitchname in pitchnames
            )

        def convert_pitchname_to_notename(pitchname: str, symbol_octave: str) -> str:
            # <N>
            if symbol_octave.find("<N>") >= 0:
                return symbol_octave.replace("<N>", pitchname, 1)
            # <n>
            elif symbol_octave.find("<n>") >= 0:
                return symbol_octave.replace("<n>", pitchname, 1)
            else:
                return symbol_octave + pitchname

        temp_name2number = {
            convert_pitchname_to_notename(
                pitchname, symbol
            ): convert_pitchclass_to_notenumber(pitchclass, octave)
            for pitchname, pitchclass in self.pitchclass.name2class.items()
            for octave, symbol in enumerate(self.symbols_octave)
        }
        temp_number2name = {
            convert_pitchclass_to_notenumber(
                pitchclass, octave
            ): convert_pitchnames_to_notenames(pitchnames, symbol)
            for pitchclass, pitchnames in self.pitchclass.class2name.items()
            for octave, symbol in enumerate(self.symbols_octave)
        }

        # adjust notenumber
        ref_pitchname = self.pitchclass.symbols_pitchclass[0]
        ref_octave_notename = convert_pitchname_to_notename(
            ref_pitchname, self.symbols_octave[self.reference_octave]
        )
        adjust_notenumber = (
            self.reference_notenumber - temp_name2number[ref_octave_notename]
        )

        name2number = {}
        number2name = {}
        for allowed_notenumber in self.symbols_notenumber:
            if allowed_notenumber not in temp_number2name:
                continue
            notenames = temp_number2name[allowed_notenumber]
            number2name[allowed_notenumber + adjust_notenumber] = notenames
            for notename in notenames:
                name2number[notename] = allowed_notenumber + adjust_notenumber

        object.__setattr__(self, "adjust_notenumber", adjust_notenumber)
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
