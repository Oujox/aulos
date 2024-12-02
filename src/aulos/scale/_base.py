from abc import abstractmethod

from ..note._base import BaseNote


class BaseScale:

    @property
    @abstractmethod
    def diatonics(self) -> list[BaseNote]: ...
