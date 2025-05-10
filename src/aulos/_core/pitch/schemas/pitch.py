from dataclasses import dataclass

from aulos._core.schema import Schema

OVERTONE_RATIO = 2.0


def normalize_to_overtone_ratio(ratio: float) -> float:
    while not (1 <= ratio <= OVERTONE_RATIO):
        ratio = ratio / 2 if ratio > OVERTONE_RATIO else ratio * 2
    return ratio


@dataclass(init=False, frozen=True, slots=True)
class PitchSchema(Schema):
    def __init__(self) -> None:
        super(Schema, self).__init__()

    def validate(self) -> None:
        pass

    @classmethod
    def get_equal_tempered_ratios(cls, n: int) -> tuple[float, ...]:
        return cls.get_pitch_ratios(n, 1 / n)

    @classmethod
    def get_pythagorean_ratios(cls, n: int) -> tuple[float, ...]:
        return cls.get_pitch_ratios(n, 3 / 2)

    @classmethod
    def get_meantone_ratios(cls, n: int) -> tuple[float, ...]:
        return cls.get_pitch_ratios(n, 5 / 4)

    @classmethod
    def get_pitch_ratios(cls, n: int, ratio: float) -> tuple[float, ...]:
        return tuple(normalize_to_overtone_ratio(ratio**i) for i in range(n))
