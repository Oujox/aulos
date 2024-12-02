import typing as t
from abc import ABCMeta, abstractmethod


class BaseNote(metaclass=ABCMeta):

    @abstractmethod
    def __int__(self) -> int: ...

    @property
    @abstractmethod
    def pitchname(self) -> str: ...

    @property
    @abstractmethod
    def pitchclass(self) -> int: ...
