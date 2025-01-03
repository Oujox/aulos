import typing as t
from collections import deque

# from .array import inplace


def inplace[T](sequence: t.MutableSequence[T], f: t.Callable[[T], T]):
    for i in range(len(sequence)):
        sequence[i] = f(sequence[i])


def sign(num: int) -> int:
    return 1 if num > 0 else -1 if num < 0 else 0


class Intervals(t.Sequence):
    def __init__(self, sequence: t.Sequence[int]):
        self._interval = deque(sequence)

    def rotate(self, shift: int = 0):
        self._interval.rotate(shift)


class Positions(t.Sequence[int]):
    def __init__(self, sequence: t.Sequence[int]):
        self._interval = deque(sequence)

    def __len__(self) -> int:
        return self._interval.__len__()

    def __getitem__(self, key: int | slice) -> int | t.Sequence[int]:

        return self._interval.__getitem__(key)

    def rotate(self, shift: int = 0):
        start = self._interval[0] * -sign(shift)
        inplace(self._interval, lambda x: x + start)
        self._interval.rotate(shift)


print(Positions([0, 2, 4, 5, 7, 9, 11]))
