from dataclasses import dataclass

from .settings.note import NoteSetting
from .settings.pitchclass import PitchClassSetting


@dataclass(frozen=True)
class Setting:
    pitchclass: PitchClassSetting
    note: NoteSetting
