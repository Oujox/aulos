import pathlib
import typing as t
from contextlib import ContextDecorator
from contextvars import ContextVar

from .._core import SettingMT


@t.final
class Context(ContextDecorator):

    setting: t.Final[ContextVar[SettingMT]] = ContextVar("setting")

    def __init__(self, path: pathlib.Path) -> None:
        self.load(path)

    def load(self, path: pathlib.Path) -> t.Self:
        self.__token = self.setting.set(SettingMT.from_path(path))
        return self

    def __enter__(self) -> t.Self:
        return self

    def __exit__(self, *tracebacks):
        self.setting.reset(self.__token)
