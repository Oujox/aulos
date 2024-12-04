from dataclasses import dataclass, field
from itertools import accumulate, chain


@dataclass(frozen=True)
class AccidentalSymbolSetting:
    sharp: str
    flat: str


@dataclass(frozen=True)
class AccidentalSetting:
    limit: int
    symbol: AccidentalSymbolSetting


@dataclass(frozen=True)
class PitchClassSetting:
    intervals: tuple[int]
    symbols: tuple[str]
    accidental: AccidentalSetting

    semitone: int = field(init=False)
    positions: tuple[int] = field(init=False)
    name2class: dict[str, int] = field(init=False)
    class2name: dict[int, tuple[str]] = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "semitone", sum(self.intervals))
        object.__setattr__(
            self, "positions", tuple(accumulate((0,) + self.intervals[:-1]))
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


def create_upper_sequences(setting: PitchClassSetting) -> list[list[str]]:
    sequences = []
    for i in range(1, setting.accidental.limit + 1):
        sequence = create_symbol_sequence(
            setting, suffix=setting.accidental.symbol.sharp * i
        )
        for _ in range(i):
            sequence.insert(0, sequence.pop())
        sequences.append(sequence)
    return sequences


def create_lower_sequences(setting: PitchClassSetting) -> list[list[str]]:
    sequences = []
    for i in range(1, setting.accidental.limit + 1):
        sequence = create_symbol_sequence(
            setting, suffix=setting.accidental.symbol.flat * i
        )
        for _ in range(i):
            sequence.append(sequence.pop(0))
        sequences.append(sequence)
    return sequences


def create_symbol_sequence(
    setting: PitchClassSetting, *, prefix: str = "", suffix: str = ""
) -> list[str]:
    sequence = []
    for deg in range(setting.semitone):
        if deg in setting.positions:
            index = setting.positions.index(deg)
            sequence.append(prefix + setting.symbols[index] + suffix)
        else:
            sequence.append(None)
    return sequence
