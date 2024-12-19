from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NotePresentationReferenceSetting:
    number: int
    symbol: str


@dataclass(frozen=True, slots=True)
class NoteTunerReferenceSetting:
    hz: float
    number: int


@dataclass(frozen=True, slots=True)
class NoteNumberSetting:
    min: int
    max: int


@dataclass(frozen=True, slots=True)
class NotePresentationSetting:
    name: str
    symbols: tuple[str]
    reference: NotePresentationReferenceSetting


@dataclass(frozen=True, slots=True)
class NoteTunerSetting:
    reference: NoteTunerReferenceSetting


@dataclass(frozen=True, slots=True)
class NoteSetting:
    notenumber: NoteNumberSetting
    presentation: NotePresentationSetting
    tuner: NoteTunerSetting
