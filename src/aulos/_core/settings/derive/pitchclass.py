from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass
from itertools import accumulate, chain

if TYPE_CHECKING:
    from ...setting import Setting
    from ..pitchclass import PitchClassSetting


@dataclass(frozen=True, init=False)
class PitchClassSettingDerive:

    semitone: int
    positions: tuple[int]
    name2class: dict[str, int]
    class2name: dict[int, tuple[str | None]]

    def __init__(self, setting: Setting):
        object.__setattr__(self, "semitone", sum(setting.pitchclass.intervals))
        object.__setattr__(
            self,
            "positions",
            tuple(accumulate((0,) + setting.pitchclass.intervals[:-1])),
        )

        accidental_no_sequence = self._create_symbol_sequence(setting.pitchclass)
        accidental_upper_sequences = self._create_upper_sequences(setting.pitchclass)
        accidental_lower_sequences = self._create_lower_sequences(setting.pitchclass)
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

    def _create_upper_sequences(self, setting: PitchClassSetting) -> list[list[str]]:
        sequences = []
        for i in range(1, setting.accidental.limit + 1):
            sequence = self._create_symbol_sequence(
                setting, suffix=setting.accidental.symbol.sharp * i
            )
            for _ in range(i):
                sequence.insert(0, sequence.pop())
            sequences.append(sequence)
        return sequences

    def _create_lower_sequences(self, setting: PitchClassSetting) -> list[list[str]]:
        sequences = []
        for i in range(1, setting.accidental.limit + 1):
            sequence = self._create_symbol_sequence(
                setting, suffix=setting.accidental.symbol.flat * i
            )
            for _ in range(i):
                sequence.append(sequence.pop(0))
            sequences.append(sequence)
        return sequences

    def _create_symbol_sequence(
        self, setting: PitchClassSetting, *, prefix: str = "", suffix: str = ""
    ) -> list[str]:
        sequence = []
        for deg in range(self.semitone):
            if deg in self.positions:
                index = self.positions.index(deg)
                sequence.append(prefix + setting.symbols[index] + suffix)
            else:
                sequence.append(None)
        return sequence
