import json
import os
import tomllib
import typing as t
from dataclasses import dataclass
from pathlib import Path

from .utils import from_dict


@dataclass(frozen=True, slots=True)
class Setting:
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
