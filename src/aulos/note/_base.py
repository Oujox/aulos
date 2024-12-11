import typing as t
from abc import ABCMeta, abstractmethod


class BaseNote(metaclass=ABCMeta):

    @abstractmethod
    def __int__(self) -> int: ...
