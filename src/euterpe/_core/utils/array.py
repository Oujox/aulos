import typing as t
from collections import deque


def index[T](list: list[T], target: T) -> t.Optional[int]:
    if target not in list:
        return None
    return list.index(target)


def rotated[T](iterable: t.Iterable[T], shift: int = 0) -> tuple[T, ...]:
    rotated = deque(iterable)
    rotated.rotate(shift)
    return tuple(rotated)
