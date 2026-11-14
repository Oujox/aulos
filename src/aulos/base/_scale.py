"""主音と一周期内の度数列からなる音階."""

from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Self

from aulos.base._chord import Chord
from aulos.base._collection import _Collection
from aulos.core.chain import ChainInterval
from aulos.core.errors import NotationError
from aulos.core.notation import Interval

if TYPE_CHECKING:
    from aulos.base._definition import NotationTag
    from aulos.base._pitch import Pitch


class Scale[N: NotationTag](_Collection[N], abstract=True):
    """主音と同度を先頭とする一周期内の度数列。度数番号は0始まり."""

    kind = "scale"
    chord_type: type[Chord[N]] | None = None

    @classmethod
    def validate_definition(cls) -> None:
        """音階定義と、省略時に使用する和音クラスを検証する."""
        super().validate_definition()
        names = [spelling for template in cls.templates.entries for spelling in template.spellings]
        if any(not name or name != name.strip() for name in names):
            msg = "scale template names must be nonempty and have no surrounding whitespace"
            raise ValueError(msg)
        if cls.chord_type is not None:
            cls._validate_type("chord_type", Chord)

    @classmethod
    def validate_intervals(cls, intervals: tuple[Interval[N], ...]) -> None:
        """上昇する構成音が一周期に収まることを検証する."""
        super().validate_intervals(intervals)
        if intervals[-1].ratio() >= cls.notation.chain.period:
            msg = "scale degrees must lie within one period"
            raise NotationError(msg)

    @classmethod
    def parse_symbol(cls, symbol: str) -> tuple[Pitch[N], str]:
        """音域なし主音と空白で区切ったテンプレート名を読む."""
        root, rest = cls._split_root(symbol)
        if not rest.startswith(" ") or not rest[1:] or rest[1:] != rest[1:].strip():
            msg = "a scale symbol needs a root, one space, and a template name"
            raise ValueError(msg)
        return root, rest[1:]

    @property
    def tonic(self) -> Pitch[N]:
        """音階の主音を返す."""
        return self.root

    @property
    def degrees(self) -> tuple[Interval[N], ...]:
        """主音からの度数を返す."""
        return self.intervals

    def __str__(self) -> str:
        """登録構造の音階名を返す。音域は含まない."""
        return f"{self.tonic.pitch_class._render(self.symbols)} {self.template_name}"

    def degree(self, index: int) -> Pitch[N]:
        """周期をまたぐ正負の度数から音高を返す."""
        if type(index) is not int:
            msg = "a scale degree must be an integer"
            raise TypeError(msg)
        periods, position = divmod(index, len(self.degrees))
        return self.root + self.degrees[position] + Interval(self.notation, ChainInterval(0, periods))

    def mode(self, index: int) -> Self:
        """指定度数を主音として構成音を回転する。比と綴りを再解釈しない.

        周期をまたぐ ``index`` では主音の音域も変わる。
        """
        self.degree(index)
        return type(self).from_members(self.degree(index + offset) for offset in range(len(self.degrees)))

    def chord(self, degree: int = 0, count: int = 3, skip: int = 2) -> Chord[N]:
        """音階の度数を積み重ねる。標準では一つおきの三音を取る.

        ``degree`` は0始まりで周期をまたぐ値も使える。``count`` と ``skip`` は正の整数。
        和音は、定義に束ねた ``chord_type`` で作る。
        """
        if type(count) is not int or type(skip) is not int:
            msg = "chord count and skip must be integers"
            raise TypeError(msg)
        self.degree(degree)
        if count < 1 or skip < 1:
            msg = "chord count and skip must be positive"
            raise ValueError(msg)
        if self.chord_type is None:
            msg = "a concrete chord_type is required"
            raise TypeError(msg)
        return self.chord_type.from_members(self.degree(degree + offset * skip) for offset in range(count))
