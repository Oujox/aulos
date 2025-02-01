from dataclasses import dataclass
from itertools import starmap

from aulos._core import Schema
from aulos.note.schemas import PitchClassSchema


@dataclass(frozen=True, slots=True)
class ScaleSchema(Schema):
    pitchclass: PitchClassSchema

    def generate_scale_signatures(self, intervals: tuple[int, ...]) -> tuple[int, ...]:
        diff = list(
            starmap(lambda x, y: y - x, zip(self.pitchclass.intervals, intervals, strict=False)),
        )
        signature = []
        for i in range(len(self.pitchclass.intervals)):
            cur = i % len(self.pitchclass.intervals)
            next = (i + 1) % len(self.pitchclass.intervals)
            signature.append(diff[cur])
            diff[next] = diff[next] + diff[cur]
            diff[cur] = 0
        return tuple(signature[-1:] + signature[:-1])
