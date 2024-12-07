import typing as t
from pathlib import Path
from contextlib import ContextDecorator
from contextvars import ContextVar

from .._core import AulosObject, Setting


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
        return Setting.from_toml(path)

    @classmethod
    def from_json(cls, path: Path) -> t.Self:
        return Setting.from_json(path)
