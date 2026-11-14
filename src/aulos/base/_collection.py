"""根音と音程列からなる構成音列。和音と音階の共通部分."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Self

from aulos.base._definition import require_symbol
from aulos.base._pitch import Pitch
from aulos.base._structure import _Structure
from aulos.core.notation import Interval
from aulos.core.pitch import PitchValue

if TYPE_CHECKING:
    from collections.abc import Iterable

    from aulos.base._definition import NotationTag
    from aulos.base._pitch import PitchClass
    from aulos.core.temper import Tuning


@dataclass(frozen=True, init=False, eq=False)
class _Collection[N: NotationTag](_Structure[N], abstract=True):
    """根音と音程列からなる構成音列."""

    root: Pitch[N]

    def _identity(self) -> tuple[object, ...]:
        return (self.kind, self.root, self.intervals)

    def __init__(self, symbol: str) -> None:
        """文字列を解析し、定義済み構造から構成音を生成する."""
        self._require_concrete()
        require_symbol(symbol)
        root, name = self.parse_symbol(symbol)
        self._initialize(root, self._realize(name))

    @classmethod
    def parse_symbol(cls, symbol: str) -> tuple[Pitch[N], str]:
        """根音とテンプレート名を解析する。区切りは派生型が定める."""
        raise NotImplementedError

    @classmethod
    def _split_root(cls, symbol: str) -> tuple[Pitch[N], str]:
        spelling, commas, rest = cls.symbols._split_root(symbol)
        return cls.pitch_type._wrap(PitchValue.of(cls.notation, spelling, commas)), rest

    def _initialize(self, root: Pitch[N], intervals: Iterable[Interval[N]]) -> None:
        self._require_concrete()
        if not isinstance(root, Pitch):
            msg = "the root must be a Pitch"
            raise TypeError(msg)
        self.notation.require(root.notation)
        values = tuple(intervals)
        self.validate_intervals(values)
        object.__setattr__(self, "root", self.pitch_type._wrap(root._value))
        object.__setattr__(self, "intervals", values)

    @classmethod
    def from_intervals(cls, root: Pitch[N], intervals: Iterable[Interval[N]]) -> Self:
        """根音と綴り付き音程列を検証して生成する。文字列の解析は行わない."""
        result = object.__new__(cls)
        result._initialize(root, intervals)
        return result

    @classmethod
    def from_members(cls, members: Iterable[Pitch[N]]) -> Self:
        """先頭を根音として、同じ体系の構成音から生成する.

        空列は受理しない。構成音は記譜上の比で厳密な昇順でなければならず、
        並べ替えや綴りの変更は行わない。
        """
        values = tuple(members)
        if not values:
            msg = "at least one member is required"
            raise ValueError(msg)
        if any(not isinstance(member, Pitch) for member in values):
            msg = "members must be Pitch objects"
            raise TypeError(msg)
        root = values[0]
        return cls.from_intervals(root, (member - root for member in values))

    @property
    def members(self) -> tuple[Pitch[N], ...]:
        """根音と音程列から導く構成音を返す."""
        return tuple(self.root + interval for interval in self.intervals)

    @property
    def pitch_classes(self) -> tuple[PitchClass[N], ...]:
        """構成音の音高クラスを返す."""
        return tuple(member.pitch_class for member in self.members)

    @property
    def names(self) -> tuple[str, ...]:
        """コンマと音域を含む構成音名を返す."""
        return tuple(member._render(self.symbols) for member in self.members)

    def transpose(self, interval: Interval[N]) -> Self:
        """根音だけを移し、構造と具体的なサブクラスを保持する."""
        if not isinstance(interval, Interval):
            msg = "transposition needs an Interval"
            raise TypeError(msg)
        return type(self).from_intervals(self.root + interval, self.intervals)

    def degree_of(self, pitch: Pitch[N]) -> int | None:
        """音域を除いて綴りの一致する最初の構成音の添字を返す。一致しなければNone."""
        if not isinstance(pitch, Pitch):
            msg = "degree lookup needs a Pitch"
            raise TypeError(msg)
        self.notation.require(pitch.notation)
        target = self.pitch_type._wrap(pitch._value).pitch_class
        return next((index for index, member in enumerate(self.pitch_classes) if member == target), None)

    def frequencies(self, anchor: Pitch[N], anchor_hz: float, tuning: Tuning | None = None) -> tuple[float, ...]:
        """基準音 ``anchor`` の周波数 ``anchor_hz`` から、構成音の周波数をHzで返す.

        ``tuning`` の省略時は束ねた調律を使い、調律を束ねない型では指定が必要。
        """
        resolved = self._resolve_tuning(tuning)
        return tuple(resolved.frequency((member - anchor).ratio(), anchor_hz) for member in self.members)
