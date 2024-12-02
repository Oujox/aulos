import typing as t


def search[T](list: list[T], target: T) -> t.Optional[T]:
    """リスト内で同一のオブジェクトを検索。"""
    return next((item for item in list if item == target), None)


def index[T](list: list[T], target: T) -> t.Optional[int]:
    """リスト内で同一のオブジェクトの位置を検索。"""
    if target not in list:
        return None
    return list.index(target)


def rotate[T](iterable: t.Iterable[T], shift: int = 0) -> list[T]:
    """リスト内要素を回転。"""
    iterable = list(iterable)
    if 0 < shift:
        for _ in range(shift):
            iterable.insert(0, iterable.pop())
    else:
        for _ in range(-shift):
            iterable.append(iterable.pop(0))
    return iterable
