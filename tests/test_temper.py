from fractions import Fraction
from math import log2

import pytest
from hypothesis import given
from hypothesis import strategies as st

from aulos.base import ChainNotation
from aulos.base import Temperament
from aulos.base import TemperamentError
from aulos.base import Tuning
from aulos.core.chain import Spelling

vectors = st.builds(
    lambda a, b: Fraction(2) ** a * Fraction(3) ** b,
    st.integers(-5, 5),
    st.integers(-5, 5),
)


@given(vectors, vectors, st.lists(st.tuples(st.integers(-20, 20), st.integers(-20, 20)), min_size=1, max_size=3))
def test_mapping_is_linear(x, y, rows):
    temperament = Temperament((2, 3), tuple(rows))
    assert temperament.map(x * y) == tuple(a + b for a, b in zip(temperament.map(x), temperament.map(y), strict=True))
    assert temperament.map(1 / x) == tuple(-a for a in temperament.map(x))
    assert temperament.rank == len(rows)
    assert temperament.tempers_out(x) == all(value == 0 for value in temperament.map(x))


def test_mapping_respects_prime_column_order():
    forward = Temperament((2, 3), ((4, 7),))
    reversed_basis = Temperament((3, 2), ((7, 4),))
    assert forward.map(12) == reversed_basis.map(12) == (15,)


@given(vectors, st.tuples(st.integers(-20, 20), st.integers(-20, 20)), st.floats(-1200, 1200))
def test_definitions_are_independent_of_input_mutation(vector, coefficients, size):
    primes = [2, 3]
    row = list(coefficients)
    rows = [row]
    sizes = [size]
    mapping = Temperament(primes, rows)  # ty: ignore[invalid-argument-type]
    tuning = Tuning(mapping, sizes)  # ty: ignore[invalid-argument-type]
    original_mapping = Temperament((2, 3), (coefficients,))
    original_tuning = Tuning(original_mapping, (size,))
    original_hash = hash(tuning)

    primes.clear()
    row.clear()
    rows.clear()
    sizes[0] = float("nan")

    assert mapping == original_mapping
    assert tuning == original_tuning
    assert hash(tuning) == original_hash
    assert mapping.map(vector) == original_mapping.map(vector)
    assert tuning.cents(vector) == original_tuning.cents(vector)


@pytest.mark.parametrize(
    ("primes", "rows"),
    [
        ((), ((),)),
        ((2, 2), ((1, 2),)),
        ((1,), ((1,),)),
        ((4,), ((1,),)),
        ((-2,), ((1,),)),
        ((2,), ()),
        ((2, 3), ((1,),)),
    ],
)
def test_invalid_mapping(primes, rows):
    with pytest.raises(ValueError, match=r"primes|rows"):
        Temperament(primes, rows)


@pytest.mark.parametrize(("primes", "rows"), [((2.0,), ((1,),)), ((2,), ((1.5,),))])
def test_noninteger_mapping(primes, rows):
    with pytest.raises(TypeError, match="integers"):
        Temperament(primes, rows)


@given(st.integers(1, 100))
def test_equal_division_maps_period_exactly(divisions):
    mapping = Temperament.equal_division((2, 3, 5), divisions, Fraction(2))
    assert mapping.map(2) == (divisions,)
    assert mapping.map(1) == (0,)


@pytest.mark.parametrize(("divisions", "period"), [(0, 2), (-1, 2), (1, 1), (1, 0), (1, -1)])
def test_invalid_division(divisions, period):
    with pytest.raises(ValueError, match=r"positive|above"):
        Temperament.equal_division((2, 3), divisions, Fraction(period))


def test_noninteger_division():
    with pytest.raises(TypeError, match="integer"):
        Temperament.equal_division((2,), 1.5, Fraction(2))  # ty: ignore[invalid-argument-type]


def test_invalid_division_basis():
    with pytest.raises(ValueError, match="primes"):
        Temperament.equal_division((4,), 3, Fraction(2))


@given(vectors, vectors)
def test_tuning_is_additive(x, y):
    tuning = Tuning(Temperament((2, 3), ((1, 0), (0, 1))), (31.5, -12.25))
    assert tuning.cents(x * y) == pytest.approx(tuning.cents(x) + tuning.cents(y))


@pytest.mark.parametrize("sizes", [(), (1, 2), (float("nan"),), (float("inf"),)])
def test_invalid_tuning(sizes):
    with pytest.raises(ValueError, match="finite size"):
        Tuning(Temperament((2,), ((1,),)), sizes)


@given(st.integers(1, 100), st.integers(1, 100))
def test_just_tuning_keeps_exact_sizes(a, b):
    primes = tuple(prime for prime in range(2, 100) if all(prime % divisor for divisor in range(2, prime)))
    tuning = Tuning.just(primes)
    ratio = Fraction(a, b)
    assert tuning.cents(ratio) == pytest.approx(1200 * log2(ratio), abs=1e-6)
    assert tuning.frequency(ratio, 10) == pytest.approx(10 * ratio)


@pytest.mark.parametrize("ratio", [Fraction(0), Fraction(-1)])
def test_invalid_ratio(ratio):
    with pytest.raises(ValueError, match="positive"):
        Tuning.just((2,)).cents(ratio)


@pytest.mark.parametrize("anchor", [0, -1, float("inf"), float("nan")])
def test_invalid_frequency_anchor(anchor):
    with pytest.raises(ValueError, match="positive finite"):
        Tuning.just((2,)).frequency(2, anchor)


@given(st.integers(-30, 30), st.integers(0, 2))
def test_spelling_candidates_are_complete_and_ordered(step, most):
    chain = ChainNotation(Fraction(2), Fraction(3, 2), 7)
    division = Temperament.equal_division((2, 3), 12, Fraction(2))
    candidates = division._spellings(chain, step, most)
    between, alteration = division.letter_steps(chain)
    assert sum(between) == 12
    assert alteration > 0
    assert len(candidates) == len(set(candidates))
    keys = []
    for pitch in candidates:
        spelling = chain._spell(pitch)
        assert division.map(chain._ratio(pitch)) == (step,)
        assert abs(spelling.alteration) <= most
        keys.append((abs(spelling.alteration), spelling.letter))
    assert keys == sorted(keys)
    # 候補の音域は入力範囲と変化量から[-5, 5]に収まる。
    expected = {
        chain._pitch(Spelling(letter, altered, register))
        for letter in range(7)
        for altered in range(-most, most + 1)
        for register in range(-5, 6)
        if division.map(chain._ratio(chain._pitch(Spelling(letter, altered, register)))) == (step,)
    }
    assert set(candidates) == expected


def test_incompatible_spelling_mapping():
    chain = ChainNotation(Fraction(2), Fraction(3, 2), 7)
    with pytest.raises(TemperamentError):
        Temperament((2, 3), ((0, 0),))._spellings(chain, 0, 1)
    with pytest.raises(ValueError, match="negative"):
        Temperament.equal_division((2, 3), 12, Fraction(2))._spellings(chain, 0, -1)
