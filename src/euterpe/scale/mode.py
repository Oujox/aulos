import typing as t

class Mode:

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is Mode:
            raise TypeError("Mode cannot be instantiated directly.")
        return super().__new__(cls)

    def __init_subclass__(cls, *, intervals: t.Iterable[int], shift: int, **kwargs) -> None:
        kwargs.update({"intervals": intervals,"shift": shift})
        super(Mode, cls).__init_subclass__(**kwargs)

    def __str__(self) -> str:
        return "<Mode: {}>".format(self.__class__.__name__)

    def __repr__(self) -> str:
        return "<Mode: {}>".format(self.__class__.__name__)
