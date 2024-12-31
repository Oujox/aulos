from abc import abstractmethod
from typing import Sequence

from ..note._base import BaseNote


class BaseScale:
    __slots__ = ()

    @property
    @abstractmethod
    def components(self) -> Sequence[BaseNote]: ...
