import typing as t
from dataclasses import dataclass, field

from .schema import Schema
from .settings.note import NoteSetting
from .settings.pitchclass import PitchClassSetting


@dataclass(frozen=True)
class Setting:

    pitchclass: PitchClassSetting
    note: NoteSetting
