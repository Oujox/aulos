import typing as t


class classproperty[S: object, R: object]:
    def __init__(self, method: t.Callable[[S], R] | None = None) -> None:
        self.fget = method

    def __get__(self, _: object, cls: type[S] | None = None) -> R:
        if self.fget is None:
            msg = "unreadable attribute"
            raise AttributeError(msg)
        return self.fget(cls)

    def getter(self, method: t.Callable[[S], R]) -> t.Self:
        self.fget = method
        return self
