from abc import abstractmethod


class BaseNote:
    __slots__ = ()

    @abstractmethod
    def __int__(self) -> int: ...
