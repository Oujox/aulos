import typing as t
import json
import tomllib
from pathlib import Path
from contextlib import ContextDecorator
from contextvars import ContextVar
from dacite import from_dict, Config as dacite_Config

from .._core import Object, Setting
from .._core.utils import convert_lists_to_tuples


@t.final
class Context(ContextDecorator, Object):

    internal: t.Final[ContextVar[Setting]] = ContextVar("internal")

    def __init__(self, setting: Setting) -> None:
        super().__init__(setting)
        self._token = self.internal.set(setting)

    def __enter__(self) -> t.Self:
        return self

    def __exit__(self, *tracebacks):
        self.internal.reset(self._token)

    @classmethod
    def setting(self) -> t.Optional[Setting]:
        return self.internal.get(None)

    @classmethod
    def from_toml(cls, path: Path) -> t.Self:
        setting = tomllib.load(open(path, mode="rb"))

        setting = convert_lists_to_tuples(setting)
        print(setting)
        setting = from_dict(Setting, setting, dacite_Config(check_types=False))
        return cls(setting)

    @classmethod
    def from_json(cls, path: Path) -> t.Self:
        setting = json.load(open(path, mode="rb"))
        setting = convert_lists_to_tuples(setting)
        setting = from_dict(Setting, setting, dacite_Config(check_types=False))
        return cls(setting)
