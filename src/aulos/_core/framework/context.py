import typing as t
from contextlib import ContextDecorator
from contextvars import ContextVar


class Context(ContextDecorator):

    internal: t.Final[ContextVar[dict[str, t.Any]]] = ContextVar("internal")

    def __init__(self, **kwargs) -> None:
        self._token = self.internal.set(kwargs)

    def __enter__(self) -> t.Self:
        return self

    def __exit__(self, *tracebacks):
        self.internal.reset(self._token)
