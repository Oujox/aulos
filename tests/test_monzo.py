from fractions import Fraction

import pytest
from hypothesis import given
from hypothesis import strategies as st

from aulos.core.monzo import Monzo

# 試し割りの負荷を制限しつつ、分子と分母に幅広い素数を含める。
ratios = st.builds(Fraction, st.integers(1, 100), st.integers(1, 100))


def test_unit():
    assert Monzo.of(1).exponents == ()


@given(ratios)
def test_roundtrip(ratio):
    assert Monzo.of(ratio).ratio() == ratio


@given(ratios, ratios)
def test_homomorphism(a, b):
    assert Monzo.of(a * b) == Monzo.of(a) + Monzo.of(b)


@given(ratios, ratios, ratios)
def test_abelian_group(a, b, c):
    x, y, z = Monzo.of(a), Monzo.of(b), Monzo.of(c)
    assert (x + y) + z == x + (y + z)
    assert x + y == y + x
    assert x + Monzo.of(1) == x
    assert x + (-x) == Monzo.of(1)
    assert x - y == x + (-y)


@given(ratios, st.integers(-4, 4))
def test_integer_multiplication(ratio, times):
    monzo = Monzo.of(ratio)
    assert (monzo * times).ratio() == ratio**times


@given(ratios)
def test_canonical_support(ratio):
    monzo = Monzo.of(ratio)
    assert monzo.exponents == tuple(sorted(monzo.exponents))
    assert monzo.primes == frozenset(prime for prime, _ in monzo.exponents)
    assert all(exponent != 0 and monzo.exponent(prime) == exponent for prime, exponent in monzo.exponents)
    assert monzo.exponent(101) == 0
    assert (monzo - monzo).exponents == ()


@pytest.mark.parametrize("ratio", [0, -1, Fraction(-2, 3)])
def test_invalid_ratio(ratio):
    with pytest.raises(ValueError, match="positive ratio"):
        Monzo.of(ratio)
