from dataclasses import dataclass, field

from .derive.note import NoteSettingDerive


@dataclass(frozen=True)
class NotePresentationReferenceSetting:
    number: int
    symbol: str


@dataclass(frozen=True)
class NoteTunerReferenceSetting:
    hz: float


@dataclass(frozen=True)
class NoteNumberSetting:
    min: int
    max: int


@dataclass(frozen=True)
class NotePresentationSetting:
    name: str
    symbols: tuple[str]
    reference: NotePresentationReferenceSetting


@dataclass(frozen=True)
class NoteTunerSetting:
    reference: NoteTunerReferenceSetting


@dataclass(frozen=True)
class NoteSetting:
    notenumber: NoteNumberSetting
    presentation: NotePresentationSetting
    tuner: NoteTunerSetting

    derive: NoteSettingDerive = field(init=False)
