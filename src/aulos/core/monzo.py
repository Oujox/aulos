"""正の有理数の素因数指数ベクトル。ベクトルの加算が比の乗算に対応する."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import TYPE_CHECKING

from aulos.core.maths import Vector
from aulos.core.maths import factorize
from aulos.core.maths import strip_factor

if TYPE_CHECKING:
    from collections.abc import Iterable


def _positive(ratio: Fraction | int) -> Fraction:
    """比をFractionにそろえ、0以下の値を拒否する."""
    value = Fraction(ratio)
    if value <= 0:
        msg = f"{value} is not a positive ratio"
        raise ValueError(msg)
    return value


@dataclass(frozen=True, slots=True)
class Monzo:
    """``((prime, exponent), ...)`` を素数順に並べ、指数0は含まない."""

    exponents: tuple[tuple[int, int], ...]

    @classmethod
    def of(cls, ratio: Fraction | int) -> Monzo:
        """正の有理比を素因数の指数ベクトルにする."""
        value = _positive(ratio)
        exponents = dict(factorize(value.numerator))
        for prime, exponent in factorize(value.denominator).items():
            exponents[prime] = exponents.get(prime, 0) - exponent
        return cls._from(exponents)

    @classmethod
    def over(cls, ratio: Fraction | int, primes: Iterable[int]) -> Monzo | None:
        """``primes`` だけで表せる比の指数ベクトルを返す。他の素因数があればNone.

        対応外の素因数を含む残余は、因数分解せずに拒否する。
        """
        value = _positive(ratio)
        numerator, denominator = value.numerator, value.denominator
        exponents: dict[int, int] = {}
        for prime in primes:
            numerator, above = strip_factor(numerator, prime)
            denominator, below = strip_factor(denominator, prime)
            exponents[prime] = above - below
        return cls._from(exponents) if numerator == denominator == 1 else None

    @classmethod
    def _from(cls, exponents: dict[int, int]) -> Monzo:
        return cls(tuple(sorted((prime, exponent) for prime, exponent in exponents.items() if exponent)))

    @property
    def primes(self) -> frozenset[int]:
        """指数が0でない素数の集合を返す."""
        return frozenset(prime for prime, _ in self.exponents)

    def exponent(self, prime: int) -> int:
        """指定した素数の指数を返す。含まれない素数は0とする."""
        return dict(self.exponents).get(prime, 0)

    def vector(self, primes: Iterable[int]) -> Vector:
        """``primes`` の順に指数を並べたベクトルを返す。含まれない素数は0とする."""
        exponents = dict(self.exponents)
        return Vector(tuple(exponents.get(prime, 0) for prime in primes))

    def ratio(self) -> Fraction:
        """指数ベクトルを正の有理比に戻す."""
        value = Fraction(1)
        for prime, exponent in self.exponents:
            value *= Fraction(prime) ** exponent
        return value

    def __add__(self, other: Monzo) -> Monzo:
        exponents = dict(self.exponents)
        for prime, exponent in other.exponents:
            exponents[prime] = exponents.get(prime, 0) + exponent
        return Monzo._from(exponents)

    def __neg__(self) -> Monzo:
        return Monzo(tuple((prime, -exponent) for prime, exponent in self.exponents))

    def __sub__(self, other: Monzo) -> Monzo:
        return self + -other

    def __mul__(self, times: int) -> Monzo:
        return Monzo._from({prime: exponent * times for prime, exponent in self.exponents})
