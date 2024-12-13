import typing as t
from contextlib import ContextDecorator
from contextvars import ContextVar

from ..setting import Setting


class Context(ContextDecorator):

    setting: t.ClassVar[ContextVar[Setting]] = ContextVar("setting")
    data: t.ClassVar[ContextVar[dict[str, t.Any]]] = ContextVar("data")

    def __init__(
        self,
        setting: t.Optional[Setting] = None,
        **data,
    ) -> None:
        self.__setting = self.setting.set(setting or Setting.default())
        self.__data = self.data.set(data)

    def __enter__(self) -> t.Self:
        return self

    def __exit__(self, *tracebacks):
        self.setting.reset(self.__setting)
        self.data.reset(self.__data)
