"""生成音程の連鎖が張る格子.

点 ``(generators, periods)`` の原点からの比は ``generator ** generators * period ** periods``。
連鎖内の点は互いに異なり、どの点が同音になるかは調律写像が決める。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Literal

from aulos.core.errors import NotationError
from aulos.core.maths import Matrix
from aulos.core.maths import coprime
from aulos.core.maths import reduce_into_period
from aulos.core.monzo import Monzo

if TYPE_CHECKING:
    from fractions import Fraction


@dataclass(frozen=True, slots=True)
class ChainInterval:
    """生成音程と周期の符号付き個数で表す連鎖上の音程."""

    generators: int
    periods: int

    def __add__(self, other: ChainInterval) -> ChainInterval:
        """二つの音程を重ねた音程を返す."""
        return ChainInterval(self.generators + other.generators, self.periods + other.periods)

    def __sub__(self, other: ChainInterval) -> ChainInterval:
        """``other`` を逆向きに重ねた音程を返す."""
        return ChainInterval(self.generators - other.generators, self.periods - other.periods)

    def __neg__(self) -> ChainInterval:
        """逆向きの音程を返す."""
        return ChainInterval(-self.generators, -self.periods)


@dataclass(frozen=True, slots=True)
class ChainPitch:
    """生成音程と周期の符号付き個数で表す連鎖上の音高位置."""

    generators: int
    periods: int

    def __add__(self, interval: ChainInterval) -> ChainPitch:
        """音程だけ移した音高位置を返す."""
        return ChainPitch(self.generators + interval.generators, self.periods + interval.periods)

    def __sub__(self, other: ChainPitch) -> ChainInterval:
        """``other`` からこの音高位置までの音程を返す."""
        return ChainInterval(self.generators - other.generators, self.periods - other.periods)


@dataclass(frozen=True, slots=True)
class Spelling:
    """``letter`` は原点の文字を0とする高さ順の位置、``register`` は原点の文字から数えた周期."""

    letter: int
    alteration: int
    register: int


@dataclass(frozen=True, slots=True)
class Quality:
    """音程の性質。完全・長・短・増・減を、系と基準からの変化量で表す.

    ``kind`` が ``"perfect"`` の音程は、同度・生成音程・その転回と同じ文字幅を持ち、
    ``offset`` は完全を0、増を1、減を-1とする。``"imperfect"`` の音程は長を0、短を-1、
    増を1、減を-2とする。``offset`` は変化音程一つにつき1だけ変わる。
    """

    kind: Literal["perfect", "imperfect"]
    offset: int


def _lattice_basis(generator: Monzo, period: Monzo) -> Matrix:
    """列が生成音程と周期、行が両者の素数(昇順)に対応する指数の行列を返す.

    この行列がユニモジュラであることが、二素数の比の基底を成す条件になる。
    素数が二つでなければ正方行列にならず、ユニモジュラでもない。
    """
    primes = sorted(generator.primes | period.primes)
    return Matrix.from_columns(generator.vector(primes), period.vector(primes))


@dataclass(frozen=True, slots=True, init=False)
class ChainNotation:
    """原点から ``generator`` を連ねた最初の ``size`` 音を ``period`` 内の文字とする.

    文字配置はモーメント・オブ・シンメトリーの条件を満たす必要がある。
    満たさないと文字と変化量の加算が整合しないため、定義を拒否する。
    """

    period: Fraction
    generator: Fraction
    size: int
    span: int
    """生成音程1個で進む文字数。下行する生成音程では負になる."""
    naturals: tuple[int, ...]
    """高さ順に並べた各自然音の連鎖番号."""
    _lattice: tuple[Monzo, Monzo]
    _inverse: Matrix
    """素数の指数を格子の座標 ``(generators, periods)`` に戻す、基底行列の整数逆行列."""
    rise: int
    """連鎖を ``size`` 個進めて同じ文字が高くなるなら+1、低くなるなら-1."""

    def __init__(self, period: Fraction, generator: Fraction, size: int) -> None:
        if period <= 1:
            msg = f"the period {period} is not above 1"
            raise ValueError(msg)
        if generator <= 0 or generator == 1:
            msg = f"the generator {generator} is not a positive interval other than the unison"
            raise ValueError(msg)
        if size < 2:  # noqa: PLR2004
            msg = f"{size} letters: a chain notation needs at least two"
            raise ValueError(msg)
        basis = _lattice_basis(Monzo.of(generator), Monzo.of(period))
        if not basis.is_unimodular:
            msg = f"{generator} and {period} are not a basis of the ratios of two primes"
            raise NotationError(msg)
        links = range(size)
        reduced = {link: reduce_into_period(generator**link, period) for link in links}
        if len({reduction.value for reduction in reduced.values()}) != size:
            msg = f"the generator {generator} gives the same pitch twice within {size} links"
            raise NotationError(msg)
        naturals = tuple(sorted(links, key=lambda link: reduced[link].value))
        span = naturals.index(1) - reduced[1].periods * size
        places = {link: link * span + reduced[link].periods * size for link in links}
        if not coprime(span, size) or any(places[link] != naturals.index(link) for link in links):
            msg = f"{size} links of {generator} in {period} are not a moment of symmetry: letters would not add up"
            raise NotationError(msg)
        object.__setattr__(self, "period", period)
        object.__setattr__(self, "generator", generator)
        object.__setattr__(self, "size", size)
        object.__setattr__(self, "span", span)
        object.__setattr__(self, "naturals", naturals)
        object.__setattr__(self, "_lattice", (Monzo.of(generator), Monzo.of(period)))
        object.__setattr__(self, "_inverse", basis.inverse())
        chroma = generator**size * period ** (-span)
        object.__setattr__(self, "rise", 1 if chroma > 1 else -1)

    @property
    def alteration(self) -> ChainInterval:
        """文字を保って一段上げる変化音程(アポトメ)を返す."""
        return ChainInterval(self.rise * self.size, -self.rise * self.span)

    def invert(self, interval: ChainInterval) -> ChainInterval:
        """``interval`` と合わせて一周期になる転回音程を返す."""
        return ChainInterval(-interval.generators, 1 - interval.periods)

    @property
    def _primes(self) -> frozenset[int]:
        generator, period = self._lattice
        return generator.primes | period.primes

    def _monzo(self, point: ChainPitch | ChainInterval) -> Monzo:
        generator, period = self._lattice
        return generator * point.generators + period * point.periods

    @property
    def _basis(self) -> Matrix:
        """格子の座標 ``(generators, periods)`` を素数の指数に写す行列."""
        return _lattice_basis(*self._lattice)

    def _locate(self, monzo: Monzo) -> ChainInterval | None:
        """指数ベクトルに対応する格子上の音程を返す。格子外ならNone."""
        # 基底行列は定義時にユニモジュラと検証済みのため、整数の逆行列で座標に戻せる。
        exponents = monzo.vector(sorted(self._primes))
        generators, periods = self._inverse @ exponents
        found = ChainInterval(generators, periods)
        # 第三の素数を含む値は上の二成分だけでは検出できない。
        return found if self._monzo(found) == monzo else None

    def _ratio(self, point: ChainPitch | ChainInterval) -> Fraction:
        return self.generator**point.generators * self.period**point.periods

    def _steps(self, point: ChainPitch | ChainInterval) -> int:
        return point.generators * self.span + point.periods * self.size

    def _spell(self, pitch: ChainPitch | ChainInterval) -> Spelling:
        register, letter = divmod(self._steps(pitch), self.size)
        alteration, rest = divmod(pitch.generators - self.naturals[letter], self.size)
        alteration *= self.rise
        if rest:
            msg = "unreachable: a moment of symmetry puts every link on its letter"
            raise AssertionError(msg)
        return Spelling(letter, alteration, register)

    def _pitch(self, spelling: Spelling) -> ChainPitch:
        if not 0 <= spelling.letter < self.size:
            msg = f"letter {spelling.letter} is not one of the {self.size} letters"
            raise ValueError(msg)
        generators = self.naturals[spelling.letter] + spelling.alteration * self.rise * self.size
        steps = spelling.register * self.size + spelling.letter
        periods, rest = divmod(steps - generators * self.span, self.size)
        if rest:
            msg = "unreachable: a moment of symmetry puts every link on its letter"
            raise AssertionError(msg)
        return ChainPitch(generators, periods)

    def _quality(self, interval: ChainInterval) -> Quality:
        """音程の性質を返す。生成音程とその転回の文字幅を完全音程とする."""
        if self.size == 2:  # noqa: PLR2004
            msg = "with two letters the generator and its inversion share a span: no size of it is the reference"
            raise NotationError(msg)
        span = self._steps(interval) % self.size
        kind: Literal["perfect", "imperfect"] = "perfect"
        if span == 0:
            reference = 0
        else:
            upper = next(link for link in range(1, self.size) if (link * self.span) % self.size == span)
            if upper == 1:
                reference = 1
            elif upper == self.size - 1:
                reference = -1
            else:
                reference, kind = upper if self.rise > 0 else upper - self.size, "imperfect"
        offset, rest = divmod(self.rise * (interval.generators - reference), self.size)
        if rest:
            msg = "unreachable: the span fixes the generators up to whole alterations"
            raise AssertionError(msg)
        return Quality(kind, offset)
