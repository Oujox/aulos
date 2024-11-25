import pathlib
import tomllib
import typing as t

from dacite import from_dict

from .bases.base import BaseMT
from .settings import ParsedSetting
from .shared import HarmonicSystem


class SettingMT(HarmonicSystem, BaseMT):

    def __init__(self, setting_dict: pathlib.Path) -> None:
        self._setting = from_dict(ParsedSetting, setting_dict)
        super().__init__(semitone=self._setting.scheme.semitone)

    @property
    def scheme(self):
        return self._setting.scheme

    @property
    def notenumber(self):
        return self._setting.notenumber

    def __eq__(self, other: t.Self) -> bool:
        return self._setting == other._setting

    def __ne__(self, other: t.Self) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return "<SettingMT>"

    def __repr__(self) -> str:
        return "<SettingMT>"

    @classmethod
    def from_path(cls, path: pathlib.Path) -> t.Self:
        setting_dict = tomllib.load(open(path, mode="rb"))
        return cls(setting_dict)
