from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AccidentalSymbolSetting:
    sharp: str
    flat: str


@dataclass(frozen=True, slots=True)
class AccidentalSetting:
    limit: int
    symbol: AccidentalSymbolSetting


@dataclass(frozen=True, slots=True)
class PitchClassSetting:
    intervals: tuple[int]
    symbols: tuple[str]
    accidental: AccidentalSetting
