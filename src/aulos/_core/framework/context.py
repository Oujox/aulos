import typing as t
from contextlib import ContextDecorator
from contextvars import ContextVar

from ..setting import Setting


class Context(ContextDecorator):

    setting: t.ClassVar[ContextVar[Setting]] = ContextVar("setting")
    coexist: t.ClassVar[ContextVar[bool]] = ContextVar("coexist")
    data: t.ClassVar[ContextVar[dict[str, t.Any]]] = ContextVar("data")

    def __init__(
        self,
        setting: t.Optional[Setting] = None,
        enable_coexistence_check: bool = False,
        **data,
    ) -> None:
        self.__setting = self.setting.set(setting or Setting.default())
        self.__coexist = self.coexist.set(enable_coexistence_check)
        self.__data = self.data.set(data)

    def __enter__(self) -> t.Self:
        return self

    def __exit__(self, *tracebacks):
        self.setting.reset(self.__setting)
        self.coexist.reset(self.__coexist)
        self.data.reset(self.__data)
