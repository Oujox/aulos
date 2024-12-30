import typing as t
from collections import deque


def index[T](list: list[T], target: T) -> t.Optional[int]:
    if target not in list:
        return None
    return list.index(target)


def rotated[T](sequence: t.Sequence[T], shift: int = 0) -> tuple[T, ...]:
    rotated = deque(sequence)
    rotated.rotate(shift)
    return tuple(rotated)
