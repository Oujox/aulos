from abc import abstractmethod


class BaseChord:
    __slots__ = ()

    @abstractmethod
    @property
    def components(self) -> tuple: ...
