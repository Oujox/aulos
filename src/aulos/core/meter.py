"""小節を段階的に分割する拍子.

小節内のパルスは巡回群を成し、各階層の格子はその部分群の列になる。
浅い階層に乗る時刻ほど拍として強い。
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from aulos.core.errors import RhythmError
from aulos.core.time import Duration
from aulos.core.time import Position

_SMALLEST_DIVISION = 2


@dataclass(frozen=True, slots=True)
class Meter:
    """各階層の分割数と、最下層のパルスの音価からなる拍子.

    ``divisions`` は小節から順に各階層を何分割するかを表す。八分音符をパルスとすると、
    6/8は ``Meter((2, 3), eighth)``、3/4は ``Meter((3, 2), eighth)`` で、小節の長さは同じでも階層が異なる。
    """

    divisions: tuple[int, ...]
    pulse: Duration

    def __post_init__(self) -> None:
        object.__setattr__(self, "divisions", tuple(self.divisions))
        if any(type(division) is not int for division in self.divisions) or not isinstance(self.pulse, Duration):
            msg = "a meter needs integer divisions and a Duration pulse"
            raise TypeError(msg)
        if not self.divisions or any(division < _SMALLEST_DIVISION for division in self.divisions):
            msg = "a meter needs divisions of two or more"
            raise ValueError(msg)
        if self.pulse <= Duration(0):
            msg = "the pulse must be a positive duration"
            raise ValueError(msg)

    @property
    def pulses(self) -> int:
        """一小節のパルス数を返す."""
        return math.prod(self.divisions)

    @property
    def bar(self) -> Duration:
        """一小節の音価を返す."""
        return self.pulse * self.pulses

    def unit(self, level: int) -> Duration:
        """階層 ``level`` の一単位の音価を返す。0は小節、``len(divisions)`` はパルス."""
        if type(level) is not int:
            msg = "a level must be an integer"
            raise TypeError(msg)
        if not 0 <= level <= len(self.divisions):
            msg = f"level {level}: the meter has levels 0 to {len(self.divisions)}"
            raise ValueError(msg)
        return self.bar / math.prod(self.divisions[:level])

    def position(self, bar: int, pulse: int = 0) -> Position:
        """原点を第0小節の頭として、小節番号とパルス番号から時刻を返す."""
        if type(bar) is not int or type(pulse) is not int:
            msg = "bar and pulse numbers must be integers"
            raise TypeError(msg)
        return Position(0) + self.bar * bar + self.pulse * pulse

    def locate(self, position: Position) -> tuple[int, Duration]:
        """時刻を、小節番号と小節の頭からの音価に分ける."""
        if not isinstance(position, Position):
            msg = "a meter locates a Position"
            raise TypeError(msg)
        bar, offset = divmod(position.value, self.bar.value)
        return int(bar), Duration(offset)

    def level(self, position: Position) -> int:
        """時刻が乗る最も浅い階層を返す。0は小節の頭で、数が大きいほど弱い.

        パルスの格子に乗らない時刻は拒否する。
        """
        _, offset = self.locate(position)
        for level in range(len(self.divisions) + 1):
            if (offset / self.unit(level)).denominator == 1:
                return level
        msg = "the position lies between the pulses of the meter"
        raise RhythmError(msg)

    @property
    def weights(self) -> tuple[int, ...]:
        """一小節の各パルスの強さを返す。小節の頭が最大で、最下層だけに乗るパルスは0."""
        depth = len(self.divisions)
        return tuple(depth - self.level(self.position(0, pulse)) for pulse in range(self.pulses))
