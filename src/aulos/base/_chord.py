"""根音・構造・最低音からなる和音.

構造(根音からの音程列)と配置(どの音を最低音にするか)を分けて持つ。
最低音を変えても構造と和音名は変わらず、構成音の並びだけが変わる。
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import TYPE_CHECKING
from typing import ClassVar
from typing import Self

from aulos.base._collection import _Collection
from aulos.base._definition import require_symbol
from aulos.base._pitch import Pitch
from aulos.base._pitch import PitchClass
from aulos.base._structure import Voicing
from aulos.core.chain import ChainInterval
from aulos.core.errors import RepresentationError
from aulos.core.maths import reduce_into_period
from aulos.core.notation import Interval

if TYPE_CHECKING:
    from collections.abc import Iterable

    from aulos.base._definition import NotationTag


class _ChordDefinition[N: NotationTag](_Collection[N], abstract=True):
    """和音の設定を、値を持つ ``Chord`` のdataclassフィールドにしないための中間クラス."""

    voicing_type: type[Voicing[N]] | None = None
    slash: ClassVar[str] = "/"
    """コード記号で、根音側の記号と最低音を区切る文字列."""

    @classmethod
    def validate_definition(cls) -> None:
        """根音の記号・テンプレート名・最低音の区切りが曖昧にならないことを検証する."""
        super().validate_definition()
        marks = (
            cls.symbols.raised,
            cls.symbols.lowered,
            *(mark for comma in cls.symbols.commas for mark in (comma.raised, comma.lowered)),
        )
        names = [spelling for template in cls.templates.entries for spelling in template.spellings]
        if any(name.startswith(marks) for name in names):
            msg = "a chord template name cannot start with a root alteration or comma mark"
            raise RepresentationError(msg)
        if not isinstance(cls.slash, str):
            msg = "the slash must be a string"
            raise TypeError(msg)
        if not cls.slash or any(cls.slash in text for text in (*cls.symbols.letters, *marks, *names)):
            msg = "the slash must be nonempty and occur in no pitch symbol or chord template name"
            raise RepresentationError(msg)
        if cls.voicing_type is not None:
            cls._validate_type("voicing_type", Voicing)

    @classmethod
    def parse_symbol(cls, symbol: str) -> tuple[Pitch[N], str]:
        """音域なし根音に続く文字列全体をテンプレート名として読む."""
        return cls._split_root(symbol)


@dataclass(frozen=True, init=False, eq=False)
class Chord[N: NotationTag](_ChordDefinition[N], abstract=True):
    """根音と綴り付き音程列、および最低音の音高クラスからなる和音.

    ``intervals`` は根音からの構造で、最低音によらない。``members`` は最低音から上へ並べた構成音。
    最低音が根音と同じ音高クラスなら基本形で、``members`` は根音から始まる。
    """

    kind = "chord"
    bass: PitchClass[N]
    """最低音の音高クラス。基本形では根音の音高クラスに等しい."""

    def __init__(self, symbol: str) -> None:
        """``"Cm7"`` や、最低音を指定した ``"Cm7/Eb"`` のようなコード記号から生成する."""
        self._require_concrete()
        require_symbol(symbol)
        head, separator, tail = symbol.partition(self.slash)
        root, name = self.parse_symbol(head)
        bass = self.pitch_type.pitch_class_type(tail) if separator else None
        self._initialize(root, self._realize(name), bass)

    def _initialize(self, root: Pitch[N], intervals: Iterable[Interval[N]], bass: PitchClass[N] | None = None) -> None:
        super()._initialize(root, intervals)
        if bass is None:
            bass = self.root.pitch_class
        elif not isinstance(bass, PitchClass):
            msg = "the bass must be a PitchClass"
            raise TypeError(msg)
        self.notation.require(bass.notation)
        object.__setattr__(self, "bass", self.pitch_type.pitch_class_type._wrap(bass._value))

    def _identity(self) -> tuple[object, ...]:
        return (*super()._identity(), self.bass)

    def _rebuilt(self, root: Pitch[N], bass: PitchClass[N]) -> Self:
        result = object.__new__(type(self))
        result._initialize(root, self.intervals, bass)
        return result

    def over(self, bass: PitchClass[N]) -> Self:
        """構造を保ったまま、最低音を ``bass`` に置き換えた和音を返す.

        構成音にない音高クラスも指定でき、その場合は最低音として加わる。
        """
        return self._rebuilt(self.root, bass)

    def inversion(self, index: int) -> Self:
        """``intervals`` の ``index`` 番目の構成音を最低音とする転回形を返す。0は基本形."""
        if type(index) is not int:
            msg = "an inversion index must be an integer"
            raise TypeError(msg)
        if not 0 <= index < len(self.intervals):
            msg = f"inversion {index}: the chord has {len(self.intervals)} members"
            raise ValueError(msg)
        return self.over((self.root + self.intervals[index]).pitch_class)

    def transpose(self, interval: Interval[N]) -> Self:
        """根音と最低音を同じ音程で移し、構造と具体的なサブクラスを保持する."""
        if not isinstance(interval, Interval):
            msg = "transposition needs an Interval"
            raise TypeError(msg)
        return self._rebuilt(self.root + interval, self.bass + interval)

    def _lift(self, interval: Interval[N], floor: Fraction) -> Interval[N]:
        """``floor`` 以上で一周期未満の高さになるよう、音程を周期単位で移す."""
        turns = reduce_into_period(interval.ratio() / floor, self.notation.chain.period).periods
        return interval + Interval(self.notation, ChainInterval(0, turns))

    @property
    def _arrangement(self) -> tuple[Interval[N], ...]:
        """最低音から上へ並べた、根音からの音程列を返す.

        最低音は根音以上で一周期未満の高さに置き、それより低い構成音は周期単位で上へ移す。
        基本形では ``intervals`` に等しい。
        """
        if self.bass == self.root.pitch_class:
            return self.intervals
        lowest = self._lift(self.pitch_type.from_class(self.bass, self.root.register) - self.root, Fraction(1))
        floor = lowest.ratio()
        above = {interval if interval.ratio() >= floor else self._lift(interval, floor) for interval in self.intervals}
        return tuple(sorted(above | {lowest}, key=lambda interval: interval.ratio()))

    @property
    def members(self) -> tuple[Pitch[N], ...]:
        """最低音から上へ並べた構成音を返す."""
        return tuple(self.root + interval for interval in self._arrangement)

    @property
    def voicing(self) -> Voicing[N]:
        """最低音を基準とした、根音を持たない音程列を返す."""
        if self.voicing_type is None:
            msg = "a concrete voicing_type is required"
            raise TypeError(msg)
        lowest, *_ = arrangement = self._arrangement
        return self.voicing_type.from_intervals(interval - lowest for interval in arrangement)

    def __str__(self) -> str:
        """登録構造のコード記号を返す。根音の音域は含まず、基本形でなければ最低音を添える."""
        symbol = self.root.pitch_class._render(self.symbols) + self.template_name
        if self.bass == self.root.pitch_class:
            return symbol
        return symbol + self.slash + self.bass._render(self.symbols)
