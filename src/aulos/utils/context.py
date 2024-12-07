import typing as t
import json
import tomllib
from pathlib import Path
from contextlib import ContextDecorator
from contextvars import ContextVar

from .._core import AulosObject, Setting
from .._core.utils import from_dict


@t.final
class Context(ContextDecorator, AulosObject):

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
        setting = from_dict(Setting, setting)
        return cls(setting)

    @classmethod
    def from_json(cls, path: Path) -> t.Self:
        setting = json.load(open(path, mode="rb"))
        setting = from_dict(Setting, setting)
        return cls(setting)
