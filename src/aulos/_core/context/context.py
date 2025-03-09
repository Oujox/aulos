import typing as t
from contextlib import ContextDecorator
from contextvars import ContextVar
from types import TracebackType

from aulos._core.object import AulosObject


class Context(ContextDecorator):
    injectables: t.ClassVar[ContextVar[dict[str, t.Any]]] = ContextVar("injectables")

    def __init__(
        self,
        **injectables: AulosObject,
    ) -> None:
        self.__injectables = self.injectables.set(injectables)

    def __enter__(self) -> t.Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.injectables.reset(self.__injectables)
