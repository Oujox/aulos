import typing as t


class Mode:

    def __new__(cls, *args, **kwargs) -> t.Self:
        if cls is Mode:
            raise TypeError("Mode cannot be instantiated directly.")
        return super().__new__(cls)

    def __str__(self) -> str:
        return "<Mode: {}>".format(self.__class__.__name__)

    def __repr__(self) -> str:
        return "<Mode: {}>".format(self.__class__.__name__)
