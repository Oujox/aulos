from abc import ABCMeta
from dataclasses import dataclass


@dataclass(frozen=True)
class Schema(metaclass=ABCMeta):

    def validate(self) -> None: ...
    def initialize(self) -> None: ...
