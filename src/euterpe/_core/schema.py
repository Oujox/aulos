from __future__ import annotations

import typing as t
from dataclasses import dataclass
from functools import cached_property
from itertools import starmap

from .framework import InstanceCacheMeta
from .schemas.note import NoteSchema
from .schemas.pitchclass import PitchClassSchema
from .setting import Setting
from .utils import wrapped_diff


@dataclass(frozen=True, init=False)
class Schema(metaclass=InstanceCacheMeta):

    _setting: Setting
    _note: NoteSchema
    _pitchclass: PitchClassSchema

    def __init__(self, setting: Setting) -> None:
        object.__setattr__(self, "_setting", setting)
        object.__setattr__(self, "_pitchclass", PitchClassSchema(setting))
        object.__setattr__(self, "_note", NoteSchema(setting, self._pitchclass))

    def __eq__(self, other: t.Any) -> bool:
        if not isinstance(other, Schema):
            return NotImplemented
        return self._setting == other._setting

    def __ne__(self, other: t.Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return "<Schema: setting={}>".format(self._setting)

    def __repr__(self) -> str:
        return "<Schema: setting={}>".format(self._setting)

    """
    PitchClass
    """

    @property
    def semitone(self) -> int:
        return self._pitchclass.semitone

    @property
    def intervals(self) -> tuple[int, ...]:
        return self._setting.pitchclass.intervals

    @property
    def positions(self) -> tuple[int, ...]:
        return self._pitchclass.positions

    @property
    def symbols(self) -> tuple[str, ...]:
        return self._setting.pitchclass.symbols

    @cached_property
    def pitchnames(self) -> tuple[str, ...]:
        return tuple(self._pitchclass.name2class.keys())

    @cached_property
    def pitchclasses(self) -> tuple[int, ...]:
        return tuple(self._pitchclass.class2name.keys())

    def find_pitchname(self, value: str) -> str | None:
        finded = sorted(
            [pitchname for pitchname in self.pitchnames if value.find(pitchname) == 0],
            key=len,
            reverse=True,
        )
        return (finded + [None])[0]

    def convert_pitchclass_to_pitchname(
        self, pitchclass: int, accidental: int
    ) -> str | None:
        if not self.is_pitchclass(pitchclass):
            raise ValueError(f"Invalid pitchclass: '{pitchclass}'.")
        return self._pitchclass.class2name[pitchclass][
            self._setting.pitchclass.accidental.limit + accidental
        ]

    def convert_pitchclass_to_pitchnames(
        self, pitchclass: int
    ) -> tuple[str | None, ...]:
        if not self.is_pitchclass(pitchclass):
            raise ValueError(f"Invalid pitchclass: '{pitchclass}'.")
        return self._pitchclass.class2name[pitchclass]

    def convert_pitchname_to_picthclass(self, pitchname: str) -> int:
        if not self.is_pitchname(pitchname):
            raise ValueError(f"Invalid pitchname: '{pitchname}'.")
        return self._pitchclass.name2class[pitchname]

    def convert_pitchclass_to_symbol(self, pitchclass: int) -> str | None:
        if not self.is_pitchclass(pitchclass):
            raise ValueError(f"Invalid pitchclass: '{pitchclass}'.")
        return self.convert_pitchclass_to_pitchnames(pitchclass)[
            self._setting.pitchclass.accidental.limit
        ]

    def convert_pitchname_to_symbol(self, pitchname: str):
        if not self.is_pitchname(pitchname):
            raise ValueError(f"Invalid pitchname: '{pitchname}'.")
        return pitchname.replace(
            self._setting.pitchclass.accidental.symbol.sharp, ""
        ).replace(self._setting.pitchclass.accidental.symbol.flat, "")

    def is_symbol(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self._setting.pitchclass.symbols

    def is_pitchname(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.pitchnames

    def is_pitchclass(self, value: t.Any) -> t.TypeGuard[int]:
        return isinstance(value, int) and value in self.pitchclasses

    """
    Note
    """

    @cached_property
    def notenames(self) -> tuple[str, ...]:
        return tuple(self._note.name2number.keys())

    @cached_property
    def notenumbers(self) -> tuple[int, ...]:
        return tuple(self._note.number2name.keys())

    def convert_notenumber_to_notename(
        self, notenumber: int, accidental: int
    ) -> str | None:
        if not self.is_notenumber(notenumber):
            raise ValueError(f"Invalid notenumber: '{notenumber}'.")
        return self._note.number2name[notenumber][
            self._setting.pitchclass.accidental.limit + accidental
        ]

    def convert_notenumber_to_notenames(
        self, notenumber: int
    ) -> tuple[str | None, ...]:
        if not self.is_notenumber(notenumber):
            raise ValueError(f"Invalid notenumber: '{notenumber}'.")
        return self._note.number2name[notenumber]

    def convert_notename_to_notenumber(self, notename: str) -> int:
        if not self.is_notename(notename):
            raise ValueError(f"Invalid notename: '{notename}'.")
        return self._note.name2number[notename]

    def is_notename(self, value: t.Any) -> t.TypeGuard[str]:
        return isinstance(value, str) and value in self.notenames

    def is_notenumber(self, value: t.Any) -> t.TypeGuard[int]:
        return isinstance(value, int) and value in self.notenumbers

    """
    Tuner
    """

    @property
    def root_hz(self) -> float:
        return self._setting.note.tuner.reference.hz

    @property
    def root_notenumber(self) -> int:
        return self._setting.note.tuner.reference.number

    """
    Extension
    """

    def generate_key_signatures(self, pitchname: str) -> tuple[int, ...]:
        if not self.is_pitchname(pitchname):
            raise ValueError(f"Invalid pitchname: '{pitchname}'.")
        positions = []
        r_symbol = self.convert_pitchname_to_symbol(pitchname)
        r_pitchclass = self.convert_pitchname_to_picthclass(pitchname)

        idx = self.symbols.index(r_symbol)
        symbols = self.symbols[idx:] + self.symbols[:idx]

        for pos, symbol in zip(self.positions, symbols):
            n_pos = self.convert_pitchname_to_picthclass(symbol)
            a_pos = (r_pitchclass + pos) % self.semitone
            positions.append(wrapped_diff(a_pos, n_pos, self.semitone))
        return tuple(positions)

    def generate_scale_signatures(self, intervals: tuple[int, ...]) -> tuple[int, ...]:
        diff = list(starmap(lambda x, y: y - x, zip(self.intervals, intervals)))
        signature = []
        for i in range(len(self.intervals)):
            cur, next = i % len(self.intervals), (i + 1) % len(self.intervals)
            signature.append(diff[cur])
            diff[next] = diff[next] + diff[cur]
            diff[cur] = 0
        return tuple(signature[-1:] + signature[:-1])

    def convert_notenumber_to_pitchclass(self, notenumber: int) -> int:
        if not self.is_notenumber(notenumber):
            raise ValueError(f"Invalid notenumber: '{notenumber}'.")
        return notenumber % self.semitone

    def convert_pitchclass_to_notenumber(self, pitchclass: int, octnumber: int) -> int:
        if not self.is_pitchclass(pitchclass):
            raise ValueError(f"Invalid pitchclass: '{pitchclass}'.")
        return pitchclass + (self.semitone * octnumber)

    def convert_notename_to_pitchname(self, notename: str) -> str:
        if not self.is_notename(notename):
            raise ValueError(f"Invalid notename: '{notename}'.")
        notenumber = self.convert_notename_to_notenumber(notename)
        for pitchname in self.convert_notenumber_to_notenames(notenumber):
            if pitchname is not None and notename.find(pitchname) > 0:
                return pitchname
        raise ValueError("Not Reachable.")

    def convert_pitchname_to_notename(self, pitchname: str, octnumber: int) -> str:
        if not self.is_pitchname(pitchname):
            raise ValueError(f"Invalid pitchname: '{pitchname}'.")
        notesymbol = self._setting.note.presentation.symbols[octnumber]
        return create_notename_from_notesymbol(pitchname, notesymbol)


def create_notename_from_notesymbol(pitchname: str, symbol: str):
    # <N>
    if symbol.find("<N>") >= 0:
        return symbol.replace("<N>", pitchname, 1)
    # <n>
    elif symbol.find("<n>") >= 0:
        return symbol.replace("<n>", pitchname, 1)
    # Not Reachable
    raise ValueError()
