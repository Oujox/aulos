import typing as t
from collections import deque


def search[T](list: list[T], target: T) -> t.Optional[T]:
    """リスト内で同一のオブジェクトを検索。"""
    return next((item for item in list if item == target), None)


def index[T](list: list[T], target: T) -> t.Optional[int]:
    """リスト内で同一のオブジェクトの位置を検索。"""
    if target not in list:
        return None
    return list.index(target)


def rotated[T](iterable: t.Iterable[T], shift: int = 0) -> tuple[T, ...]:
    rotated = deque(iterable)
    rotated.rotate(shift)
    return tuple(rotated)
