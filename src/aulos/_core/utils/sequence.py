import typing as t


def index[T](sequence: t.Sequence[T], target: T) -> int | None:
    if target not in sequence:
        return None
    return sequence.index(target)
