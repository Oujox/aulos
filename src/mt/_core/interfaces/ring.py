from abc import ABCMeta, abstractmethod
from collections.abc import Collection
from typing import Self


class Ring(Collection, metaclass=ABCMeta):
    @abstractmethod
    def __int__(self) -> int: ...

    @abstractmethod
    def __add__(self, other: Self) -> Self: ...

    @abstractmethod
    def __sub__(self, other: Self) -> Self: ...
