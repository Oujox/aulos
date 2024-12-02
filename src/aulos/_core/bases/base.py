from abc import ABCMeta, abstractmethod
from typing import Self


class Base(metaclass=ABCMeta):
    @abstractmethod
    def __eq__(self, other: Self) -> bool: ...

    @abstractmethod
    def __ne__(self, other: Self) -> bool: ...

    @abstractmethod
    def __str__(self) -> str: ...

    @abstractmethod
    def __repr__(self) -> str: ...
