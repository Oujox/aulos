from dataclasses import dataclass

from aulos._core.scale.schemas import ScaleSchema
from aulos._core.schema import Schema


@dataclass(init=False, frozen=True, slots=True)
class ModeSchema(Schema):
    scale: ScaleSchema

    def __init__(self, /, scale: ScaleSchema) -> None:
        super(Schema, self).__init__()
        object.__setattr__(self, "scale", scale)

    def validate(self) -> None:
        pass
