import json
import os
import tomllib
import typing as t
from dataclasses import dataclass
from pathlib import Path

from .settings.derive.note import NoteSettingDerive
from .settings.derive.pitchclass import PitchClassSettingDerive
from .settings.note import NoteSetting
from .settings.pitchclass import PitchClassSetting
from .utils import from_dict


@dataclass(frozen=True)
class Setting:
    pitchclass: PitchClassSetting
    note: NoteSetting

    def __post_init__(self):
        object.__setattr__(self.pitchclass, "derive", PitchClassSettingDerive(self))
        object.__setattr__(self.note, "derive", NoteSettingDerive(self))

    @classmethod
    def default(cls) -> t.Self:
        path = Path(os.path.dirname(__file__)) / "default.toml"
        return cls.from_toml(path)

    @classmethod
    def from_dict(cls, value: dict[str, t.Any]) -> t.Self:
        return from_dict(cls, value)

    @classmethod
    def from_toml(cls, path: Path) -> t.Self:
        setting = tomllib.load(open(path, mode="rb"))
        setting = from_dict(cls, setting)
        return setting

    @classmethod
    def from_json(cls, path: Path) -> t.Self:
        setting = json.load(open(path, mode="rb"))
        setting = from_dict(cls, setting)
        return setting
