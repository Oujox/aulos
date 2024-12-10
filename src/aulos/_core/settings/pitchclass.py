from dataclasses import dataclass, field
from .derive.pitchclass import PitchClassSettingDerive


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

    derive: PitchClassSettingDerive = field(init=False)
