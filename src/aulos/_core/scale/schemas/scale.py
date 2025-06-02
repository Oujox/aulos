from dataclasses import dataclass
from itertools import starmap

from aulos._core.pitchclass import PitchClassSchema
from aulos._core.schema import Schema
from aulos._core.utils import Intervals


@dataclass(init=False, frozen=True, slots=True)
class ScaleSchema(Schema):
    pitchclass: PitchClassSchema

    def __init__(self, /, pitchclass: PitchClassSchema) -> None:
        super(Schema, self).__init__()
        object.__setattr__(self, "pitchclass", pitchclass)

    def validate(self) -> None:
        pass

    def generate_scale_signatures(self, intervals: Intervals) -> tuple[int, ...]:
        std_positions = self.pitchclass.standard_positions
        scale_positions = intervals.to_positions()
        return tuple(
            starmap(
                lambda x, y: y - x,
                zip(std_positions, scale_positions, strict=False),
            )
        )
