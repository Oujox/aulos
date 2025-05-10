from dataclasses import dataclass
from itertools import starmap

from aulos._core.note.schemas import PitchClassSchema
from aulos._core.schema import Schema


@dataclass(init=False, frozen=True, slots=True)
class ScaleSchema(Schema):
    pitchclass: PitchClassSchema

    def __init__(self, /, pitchclass: PitchClassSchema) -> None:
        super(Schema, self).__init__()
        object.__setattr__(self, "pitchclass", pitchclass)

    def validate(self) -> None:
        pass

    def generate_scale_signatures(self, intervals: tuple[int, ...]) -> tuple[int, ...]:
        diff = list(
            starmap(lambda x, y: y - x, zip(self.pitchclass.standard_intervals, intervals, strict=False)),
        )
        signature = []
        for i in range(len(self.pitchclass.standard_intervals)):
            cur = i % len(self.pitchclass.standard_intervals)
            nxt = (i + 1) % len(self.pitchclass.standard_intervals)
            signature.append(diff[cur])
            diff[nxt] = diff[nxt] + diff[cur]
            diff[cur] = 0
        return tuple(signature[-1:] + signature[:-1])
