from abc import ABCMeta, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Schema(metaclass=ABCMeta):
    @abstractmethod
    def validate(self) -> None: ...

    @abstractmethod
    def initialize(self) -> None: ...
