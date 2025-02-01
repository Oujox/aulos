import json
import tomllib
import typing as t
from dataclasses import dataclass
from pathlib import Path

from .utils import from_dict


@dataclass(frozen=True, slots=True)
class Setting:
    @classmethod
    def default(cls) -> t.Self:
        path = Path().parent / "default.toml"
        return cls.from_toml(path)

    @classmethod
    def from_dict(cls, value: dict[str, t.Any]) -> t.Self:
        return from_dict(cls, value)

    @classmethod
    def from_toml(cls, path: Path) -> t.Self:
        with Path.open(path, mode="rb") as f:
            setting = tomllib.load(f)
            return from_dict(cls, setting)

    @classmethod
    def from_json(cls, path: Path) -> t.Self:
        with Path.open(path, mode="rb") as f:
            setting = json.load(f)
            return from_dict(cls, setting)
