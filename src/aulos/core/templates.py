"""綴り付き構造のテンプレートと、構造を具体的な比にする規約."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from aulos.core.chain import ChainInterval
from aulos.core.errors import NotationError
from aulos.core.notation import Interval
from aulos.core.notation import Notation


@dataclass(frozen=True, slots=True)
class Template:
    """名前と、根音からの連鎖変位による構造.

    ``intervals`` は ``ChainInterval`` の列で、調律やコンマの選択は持たない。
    ``aliases`` は入力でだけ受け付ける別名で、表示には常に ``name`` を使う。
    音程の並びの制約は、具体クラスへ束ねる時に検証する。
    """

    name: str
    intervals: tuple[ChainInterval, ...]
    aliases: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        aliases = tuple(self.aliases)
        if any(not isinstance(name, str) for name in (self.name, *aliases)):
            msg = "a template name must be a string"
            raise TypeError(msg)
        intervals = tuple(self.intervals)
        if any(not isinstance(interval, ChainInterval) for interval in intervals):
            msg = "template intervals must be chain intervals"
            raise TypeError(msg)
        object.__setattr__(self, "intervals", intervals)
        object.__setattr__(self, "aliases", aliases)

    @property
    def spellings(self) -> tuple[str, ...]:
        """入力で受け付ける全ての名前を、``name`` を先頭にして返す."""
        return (self.name, *self.aliases)


@dataclass(frozen=True, slots=True)
class Templates:
    """重複のない名前からテンプレートを検索する定義."""

    entries: tuple[Template, ...]

    def __post_init__(self) -> None:
        entries = tuple(self.entries)
        if any(not isinstance(entry, Template) for entry in entries):
            msg = "template entries must be Template objects"
            raise TypeError(msg)
        spellings = [spelling for entry in entries for spelling in entry.spellings]
        if len(set(spellings)) != len(spellings):
            msg = "template names must be unique"
            raise ValueError(msg)
        object.__setattr__(self, "entries", entries)

    @property
    def names(self) -> tuple[str, ...]:
        """登録順のテンプレート名を返す。別名は含まない."""
        return tuple(entry.name for entry in self.entries)

    def get(self, name: str) -> Template:
        """名前か別名が完全一致するテンプレートを返す。未知の名前は拒否する."""
        for entry in self.entries:
            if name in entry.spellings:
                return entry
        msg = f"unknown template {name!r}"
        raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class Realization:
    """連鎖音程を具体的な比へ置き換える規約.

    ``ratios`` は ``(ChainInterval, 正の有理比)`` の対応列で、同じ音程を重複指定できない。
    指定しない音程は連鎖の比を保ち、置き換える時も構造上の綴りを保つ。
    """

    ratios: tuple[tuple[ChainInterval, Fraction], ...] = ()

    def __post_init__(self) -> None:
        ratios = tuple(self.ratios)
        for interval, ratio in ratios:
            if not isinstance(interval, ChainInterval) or not isinstance(ratio, (int, Fraction)):
                msg = "a realization needs chain intervals and rational ratios"
                raise TypeError(msg)
            if ratio <= 0:
                msg = "realization ratios must be positive"
                raise ValueError(msg)
        if len({interval for interval, _ in ratios}) != len(ratios):
            msg = "a realization cannot repeat an interval"
            raise ValueError(msg)
        object.__setattr__(self, "ratios", tuple((interval, Fraction(ratio)) for interval, ratio in ratios))

    def realize[N](self, notation: Notation[N], interval: ChainInterval) -> Interval[N]:
        """綴りを保った具体的な音程を返す。異なる文字への置き換えは拒否する."""
        for structural, ratio in self.ratios:
            if structural == interval:
                realized = notation.interval(ratio)
                if realized.chain != interval:
                    msg = "the realization changes the structural spelling"
                    raise NotationError(msg)
                return realized
        return Interval(notation, interval)

    def apply[N](self, notation: Notation[N], template: Template) -> tuple[Interval[N], ...]:
        """テンプレート全体を指定された体系の音程列にする."""
        return tuple(self.realize(notation, interval) for interval in template.intervals)
