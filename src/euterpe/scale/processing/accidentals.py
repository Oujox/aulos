from collections import deque
from itertools import starmap


def fix_intervals(intervals: tuple[int], scale_intervals: tuple[int]) -> tuple[int]:

    if len(intervals) > len(scale_intervals):
        pass

    if len(intervals) < len(scale_intervals):
        _stopper = 0
        _stepper = 0
        _intervals = []
        for i in range(len(scale_intervals)):
            if len(intervals) <= i - _stopper:
                _intervals.append(0)
                _stepper = 0
            elif sum(scale_intervals[i : i + _stepper + 1]) >= intervals[i - _stopper]:
                _intervals.append(intervals[i - _stopper])
                _stepper = 0
            else:
                _intervals.append(0)
                _stepper += 1
                _stopper += 1
        return tuple(_intervals)

    return intervals


def accidentals(intervals: tuple[int], shifted_intervals: tuple[int]) -> tuple[int]:

    # intaervalsを指定したスケール音程構成の要素数に合わせる
    intervals = fix_intervals(intervals, shifted_intervals)

    # 差分
    diff = list(starmap(lambda x, y: y - x, zip(intervals, shifted_intervals)))

    # 臨時記号
    accidentals = []
    for i in range(len(intervals)):
        cur, next = i % len(intervals), (i + 1) % len(intervals)
        accidentals.append(diff[cur])
        diff[next] = diff[next] + diff[cur]
        diff[cur] = 0

    return tuple(accidentals[-1:] + accidentals[:-1])


def accidentals_by_shift(intervals: tuple[int], shift: int) -> tuple[int]:
    shifted = deque(intervals, len(intervals))
    shifted.rotate(-shift)
    return accidentals(intervals, tuple(shifted))
