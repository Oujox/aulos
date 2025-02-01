import typing as t
from contextlib import ContextDecorator
from contextvars import ContextVar
from types import TracebackType

from .object import AulosObject
from .setting import Setting


class Context(ContextDecorator):
    setting: t.ClassVar[ContextVar[Setting]] = ContextVar("setting")
    data: t.ClassVar[ContextVar[dict[str, t.Any]]] = ContextVar("data")

    def __init__(
        self,
        setting: Setting,
        **data: AulosObject,
    ) -> None:
        self.__setting = self.setting.set(setting)
        self.__data = self.data.set(data)

    def __enter__(self) -> t.Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.setting.reset(self.__setting)
        self.data.reset(self.__data)
