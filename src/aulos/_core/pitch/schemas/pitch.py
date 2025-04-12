import typing as t
from dataclasses import dataclass

from aulos._core.schema import Schema

def normalize_to_overtone_ratio(ratio: float) -> float:
    while not (1 <= ratio <= 2):
        ratio = ratio / 2 if ratio > 2 else ratio * 2
    return ratio

@dataclass(frozen=True)
class PitchSchema(Schema):

    def initialize(self) -> None:
        pass

    def validate(self) -> None:
        pass

    @classmethod
    def get_equal_tempered_ratios(cls, n: int) -> tuple[float, ...]:
        return cls.get_pitch_ratios(n, 1/n)

    @classmethod
    def get_principal_ratios(cls, n: int) -> tuple[float, ...]:
        return cls.get_pitch_ratios(n, 3/2)
    
    @classmethod
    def get_pitch_ratios(cls, n: int, ratio: float) -> tuple[float, ...]:
        return tuple(normalize_to_overtone_ratio(ratio ** i) for i in range(n))
