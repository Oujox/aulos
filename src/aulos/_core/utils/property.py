import typing as t


class classproperty[R: object]:  # noqa: N801
    def __init__(self, method: t.Callable[..., R] | None = None) -> None:
        self.fget = method

    def __get__(self, _: object, cls: object | type | None = None) -> R:
        if self.fget is None:
            msg = "unreadable attribute"
            raise AttributeError(msg)
        return self.fget(cls)

    def getter(self, method: t.Callable[..., R]) -> t.Self:
        self.fget = method
        return self
