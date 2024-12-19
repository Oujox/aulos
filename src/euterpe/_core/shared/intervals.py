from __future__ import annotations

import typing as t
from collections import deque


class Intervals(t.Sequence):

    def __init__(self, iterable: t.Iterable[int]) -> None:
        self._maxlen = len(iterable)
        self._intervals = deque(iterable, len(iterable))

    def __rshift__(self, shift: int) -> Intervals:
        self._intervals.rotate(shift)
        return Intervals(self._intervals)

    def __lshift__(self, shift: int) -> Intervals:
        self._intervals.rotate(-shift)
        return Intervals(self._intervals)

    def __getitem__(self, index: int) -> int:
        return self._intervals.__getitem__(index % self._maxlen)

    def __len__(self) -> int:
        return self._maxlen

    def __str__(self) -> str:
        return self._intervals.__str__()

    def __repr__(self) -> str:
        return self._intervals.__repr__()

    def upward(self, index: int, step: int = 1):
        front = list(self._intervals)[index % self._maxlen :]
        back = list(self._intervals)[: index % self._maxlen]
        # for idx, interval in enumerate(range(self._intervals)):
        #     if idx == 1:

        return

    def downward(self, index: int, step: int = 1):
        return
