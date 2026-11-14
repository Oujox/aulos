"""記譜上の時間を秒に評価するテンポ.

音高側の調律に対応する層で、浮動小数点数はここで初めて現れる。
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import pairwise

from aulos.core.time import Duration
from aulos.core.time import Position

_SECONDS_PER_MINUTE = 60


@dataclass(frozen=True, slots=True)
class Tempo:
    """拍とする音価と、一分あたりの拍数."""

    beat: Duration
    per_minute: float

    def __post_init__(self) -> None:
        if not isinstance(self.beat, Duration) or isinstance(self.per_minute, bool):
            msg = "a tempo needs a Duration beat and a number of beats per minute"
            raise TypeError(msg)
        if self.beat <= Duration(0) or not math.isfinite(self.per_minute) or self.per_minute <= 0:
            msg = "a tempo needs a positive beat and a positive finite rate"
            raise ValueError(msg)

    def seconds(self, duration: Duration) -> float:
        """音価を秒で返す。floatで表せない長さは拒否する."""
        try:
            return float(duration / self.beat) * _SECONDS_PER_MINUTE / self.per_minute
        except OverflowError:
            msg = "the duration is outside the range of a float"
            raise ValueError(msg) from None


@dataclass(frozen=True, slots=True)
class TempoMap:
    """時刻ごとのテンポ変更。各テンポは次の変更まで一定に保つ.

    ``changes`` は ``(時刻, テンポ)`` の列で、時刻は厳密に昇順でなければならない。
    最初の変更の時刻を0秒とし、それより前の時刻は最初のテンポで負の秒に評価する。
    """

    changes: tuple[tuple[Position, Tempo], ...]

    def __post_init__(self) -> None:
        changes = tuple(tuple(change) for change in self.changes)
        if any(len(change) != 2 for change in changes) or any(  # noqa: PLR2004
            not isinstance(position, Position) or not isinstance(tempo, Tempo) for position, tempo in changes
        ):
            msg = "tempo changes must be pairs of a Position and a Tempo"
            raise TypeError(msg)
        if not changes or any(low >= high for (low, _), (high, _) in pairwise(changes)):
            msg = "a tempo map needs changes at strictly rising positions"
            raise ValueError(msg)
        object.__setattr__(self, "changes", changes)

    def seconds(self, position: Position) -> float:
        """最初の変更の時刻から ``position`` までの経過を秒で返す."""
        if not isinstance(position, Position):
            msg = "a tempo map evaluates a Position"
            raise TypeError(msg)
        elapsed = 0.0
        for (start, tempo), (end, _) in pairwise(self.changes):
            if position <= end:
                return elapsed + tempo.seconds(position - start)
            elapsed += tempo.seconds(end - start)
        start, tempo = self.changes[-1]
        return elapsed + tempo.seconds(position - start)
