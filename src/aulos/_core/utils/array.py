import typing as t
from collections import deque


def index[T](sequence: t.Sequence[T], target: T) -> int | None:
    if target not in sequence:
        return None
    return sequence.index(target)


def rotated[T](sequence: t.Sequence[T], shift: int = 0) -> tuple[T, ...]:
    rotated = deque(sequence)
    rotated.rotate(shift)
    return tuple(rotated)


def inplace[T](sequence: t.MutableSequence[T], f: t.Callable[[T], T]):
    for i in range(len(sequence)):
        sequence[i] = f(sequence[i])
