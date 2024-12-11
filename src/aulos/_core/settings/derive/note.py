from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...setting import Setting  # pragma: no cover


@dataclass(frozen=True, init=False)
class NoteSettingDerive:

    octave: int
    name2number: dict[str, int]
    number2name: dict[int, tuple[str | None]]

    def __init__(self, setting: Setting):
        min_notenumber = setting.note.notenumber.min
        max_notenumber = setting.note.notenumber.max
        ref_notenumber = setting.note.presentation.reference.number
        octave = setting.note.presentation.symbols.index(
            setting.note.presentation.reference.symbol
        )

        #
        temp_name2number = {
            self._convert_pitchname_to_notename(
                pitchname, symbol
            ): self._convert_pitchclass_to_notenumber(
                pitchclass, pitch, setting.pitchclass.derive.semitone
            )
            for pitchname, pitchclass in setting.pitchclass.derive.name2class.items()
            for pitch, symbol in enumerate(setting.note.presentation.symbols)
        }
        temp_number2name = {
            self._convert_pitchclass_to_notenumber(
                pitchclass, pitch, setting.pitchclass.derive.semitone
            ): self._convert_pitchnames_to_notenames(pitchnames, symbol)
            for pitchclass, pitchnames in setting.pitchclass.derive.class2name.items()
            for pitch, symbol in enumerate(setting.note.presentation.symbols)
        }

        # adjust notenumber
        root_pitchname = setting.pitchclass.symbols[0]
        p_ref_notename = self._convert_pitchname_to_notename(
            root_pitchname, setting.note.presentation.reference.symbol
        )
        adjust_notenumber = ref_notenumber - temp_name2number[p_ref_notename]

        #
        name2number = {}
        number2name = {}
        for allowed_notenumber in range(min_notenumber, max_notenumber + 1):
            number2name[allowed_notenumber + adjust_notenumber] = temp_number2name[
                allowed_notenumber
            ]
            for name, number in temp_name2number.items():
                if number == allowed_notenumber:
                    name2number[name] = number + adjust_notenumber

        object.__setattr__(self, "octave", octave)
        object.__setattr__(self, "name2number", name2number)
        object.__setattr__(self, "number2name", number2name)

    def _convert_pitchclass_to_notenumber(
        self, pitchclass: int, pitch: int, semitone: int
    ) -> int:
        return pitchclass + (pitch * semitone)

    def _convert_pitchname_to_notename(self, pitchname: str, symbol: str) -> str:
        # <N>
        if symbol.find("<N>") >= 0:
            return symbol.replace("<N>", pitchname, 1)
        # <n>
        elif symbol.find("<n>") >= 0:
            return symbol.replace("<n>", pitchname, 1)
        # Not Reachable
        else:
            raise ValueError()

    def _convert_pitchnames_to_notenames(
        self, pitchnames: tuple[str | None], symbol: str
    ) -> tuple[str | None]:
        return tuple(
            (
                self._convert_pitchname_to_notename(pitchname, symbol)
                if pitchname is not None
                else None
            )
            for pitchname in pitchnames
        )
