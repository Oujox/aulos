import typing as t
from dataclasses import dataclass, field

from .scheme import Scheme
from .settings.note import NoteSetting
from .settings.pitchclass import PitchClassSetting


@dataclass(frozen=True)
class Setting:

    pitchclass: PitchClassSetting
    note: NoteSetting
