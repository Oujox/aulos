from dataclasses import dataclass
from abc import ABCMeta


@dataclass(frozen=True)
class Schema(metaclass=ABCMeta):

    def validate(self) -> None: ...
    def initialize(self) -> None: ...
