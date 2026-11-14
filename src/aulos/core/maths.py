"""音楽上の概念に依存しない数学的処理.

整数論・整数の線形代数・対数と周波数の計算をここに集める。
このモジュールは他の ``aulos`` モジュールをimportしない。
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import NamedTuple

if TYPE_CHECKING:
    from collections.abc import Iterable
    from collections.abc import Iterator
    from fractions import Fraction

_CENTS_PER_OCTAVE = 1200


@dataclass(frozen=True, slots=True)
class Vector:
    """整数の列ベクトル."""

    entries: tuple[int, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "entries", tuple(self.entries))

    def __iter__(self) -> Iterator[int]:
        return iter(self.entries)

    def dot(self, other: Vector) -> int:
        """長さの等しいベクトルとの内積を返す."""
        return sum(a * b for a, b in zip(self, other, strict=True))


@dataclass(frozen=True, slots=True)
class Matrix:
    """行ごとに並べた整数行列。1行1列以上の長方形でなければならない."""

    rows: tuple[tuple[int, ...], ...]

    def __post_init__(self) -> None:
        rows = tuple(tuple(row) for row in self.rows)
        if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
            msg = "a matrix needs rows of one nonzero length"
            raise ValueError(msg)
        object.__setattr__(self, "rows", rows)

    @classmethod
    def from_columns(cls, *columns: Vector) -> Matrix:
        """列ベクトルを並べた行列を返す."""
        return cls(tuple(zip(*columns, strict=True)))

    @property
    def shape(self) -> tuple[int, int]:
        """``(行数, 列数)`` を返す."""
        return len(self.rows), len(self.rows[0])

    @property
    def is_square(self) -> bool:
        """正方行列か判定する."""
        rows, columns = self.shape
        return rows == columns

    def __matmul__(self, vector: Vector) -> Vector:
        """行列とベクトルの積。各行とベクトルの内積を並べる."""
        return Vector(tuple(Vector(row).dot(vector) for row in self.rows))

    def scaled(self, factor: int) -> Matrix:
        """全成分を ``factor`` 倍した行列を返す."""
        return Matrix(tuple(tuple(factor * entry for entry in row) for row in self.rows))

    def minor(self, row: int, column: int) -> Matrix:
        """``row`` 行と ``column`` 列を除いた小行列を返す."""
        return Matrix(
            tuple(
                tuple(entry for j, entry in enumerate(entries) if j != column)
                for i, entries in enumerate(self.rows)
                if i != row
            )
        )

    def cofactor(self, row: int, column: int) -> int:
        """余因子 ``(-1) ** (row + column) * det(minor(row, column))`` を返す."""
        sign = -1 if (row + column) % 2 else 1
        return sign * self.minor(row, column).determinant

    @property
    def determinant(self) -> int:
        """第1行に沿った余因子展開で行列式を返す."""
        self._require_square()
        if self.shape == (1, 1):
            return self.rows[0][0]
        return sum(entry * self.cofactor(0, column) for column, entry in enumerate(self.rows[0]))

    @property
    def adjugate(self) -> Matrix:
        """余因子行列の転置(随伴行列)を返す。``A @ adj(A) == det(A) * I`` を満たす."""
        self._require_square()
        size, _ = self.shape
        if size == 1:
            return Matrix(((1,),))
        return Matrix(tuple(tuple(self.cofactor(column, row) for column in range(size)) for row in range(size)))

    @property
    def is_unimodular(self) -> bool:
        """整数の逆行列を持つ(正方で行列式が+1または-1)か判定する."""
        return self.is_square and abs(self.determinant) == 1

    def inverse(self) -> Matrix:
        """ユニモジュラ行列の整数逆行列 ``adj(A) / det(A)`` を返す.

        行列式が+1または-1なので、行列式で割ることは行列式を掛けることに等しい。
        """
        if not self.is_unimodular:
            msg = "only a unimodular matrix has an integer inverse"
            raise ValueError(msg)
        return self.adjugate.scaled(self.determinant)

    def _require_square(self) -> None:
        if not self.is_square:
            msg = f"a {self.shape} matrix is not square"
            raise ValueError(msg)


class PeriodReduction(NamedTuple):
    """周期内に移した比と、移すために掛けた周期の数."""

    value: Fraction
    periods: int


def is_prime(value: int) -> bool:
    """``value`` が素数か判定する."""
    return value > 1 and all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def coprime(first: int, second: int) -> bool:
    """二つの整数が互いに素か判定する."""
    return math.gcd(first, second) == 1


def strip_factor(whole: int, divisor: int) -> tuple[int, int]:
    """``divisor`` を除いた残りと除いた回数を返す。除数を平方して巨大な数でも除算回数を抑える."""
    if whole % divisor:
        return whole, 0
    rest, count = strip_factor(whole // divisor, divisor * divisor)
    count = 2 * count + 1
    return (rest // divisor, count + 1) if rest % divisor == 0 else (rest, count)


def factorize(whole: int) -> dict[int, int]:
    """正の整数を素数ごとの指数に分解する."""
    factors: dict[int, int] = {}
    rest, prime = whole, 2
    while prime * prime <= rest:
        rest, count = strip_factor(rest, prime)
        if count:
            factors[prime] = count
        prime += 1
    if rest > 1:
        factors[rest] = 1
    return factors


def reduce_into_period(value: Fraction, period: Fraction) -> PeriodReduction:
    """``value`` を ``[1, period)`` に移した比と、適用した周期数を返す."""
    periods = 0
    while value >= period:
        value /= period
        periods -= 1
    while value < 1:
        value *= period
        periods += 1
    return PeriodReduction(value, periods)


def float_dot(counts: Iterable[int], sizes: Iterable[float]) -> float:
    """整数列と実数列の内積を返す。floatへの変換があふれたら無限大を返す."""
    try:
        return sum(count * size for count, size in zip(counts, sizes, strict=True))
    except OverflowError:
        return math.inf


def round_half_up(value: float) -> int:
    """``value`` を最も近い整数に丸める。ちょうど中間の値は大きい方に丸める."""
    return math.floor(value + 0.5)


def sizes_in_period(values: Iterable[int], period: Fraction) -> tuple[float, ...]:
    """各値の大きさを ``period`` を1とする対数尺度で返す."""
    width = math.log(period.numerator) - math.log(period.denominator)
    return tuple(math.log(value) / width for value in values)


def cents_of(value: int) -> float:
    """正の整数を比とみなした音程幅をセント単位で返す."""
    return _CENTS_PER_OCTAVE * math.log2(value)


def scale_by_cents(base: float, cents: float) -> float:
    """正の有限な ``base`` を ``cents`` だけ上げた値を返す.

    指数を合成してから評価するため、結果が表現できる限り途中であふれない。
    表現できない結果は0または無限大になる。
    """
    octaves = cents / _CENTS_PER_OCTAVE
    whole = math.floor(octaves)
    mantissa, exponent = math.frexp(base)
    try:
        return math.ldexp(mantissa * 2 ** (octaves - whole), exponent + whole)
    except OverflowError:
        return math.inf
