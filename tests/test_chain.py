from fractions import Fraction

import pytest
from hypothesis import given
from hypothesis import strategies as st

from aulos.core.chain import ChainInterval
from aulos.core.chain import ChainNotation
from aulos.core.chain import ChainPitch
from aulos.core.chain import Spelling
from aulos.core.errors import NotationError
from aulos.core.monzo import Monzo

coordinates = st.integers(-10, 10)
intervals = st.builds(ChainInterval, coordinates, coordinates)
chains = st.sampled_from(
    [
        ChainNotation(Fraction(2), generator, size)
        for generator, size in [(Fraction(3, 2), 7), (Fraction(3, 2), 5), (Fraction(4, 3), 7), (Fraction(2, 3), 7)]
    ]
)


@given(intervals, intervals, intervals)
def test_interval_group(x, y, z):
    assert (x + y) + z == x + (y + z)
    assert x + y == y + x
    assert x + ChainInterval(0, 0) == x
    assert x + (-x) == ChainInterval(0, 0)
    assert x - y == x + (-y)


@given(st.builds(ChainPitch, coordinates, coordinates), intervals, intervals)
def test_pitch_translation(pitch, x, y):
    assert (pitch + x) + y == pitch + (x + y)
    assert (pitch + x) - pitch == x


@given(chains, st.builds(ChainPitch, coordinates, coordinates))
def test_spelling_roundtrip(chain, pitch):
    spelling = chain._spell(pitch)
    assert chain._pitch(spelling) == pitch
    assert chain._steps(pitch) == spelling.register * chain.size + spelling.letter


@given(chains, st.integers(0, 4), coordinates, coordinates)
def test_pitch_roundtrip(chain, letter, alteration, register):
    spelling = Spelling(letter, alteration, register)
    assert chain._spell(chain._pitch(spelling)) == spelling


@given(chains, intervals, intervals)
def test_lattice_homomorphism(chain, x, y):
    assert chain._locate(chain._monzo(x)) == x
    assert chain._monzo(x).ratio() == chain._ratio(x)
    assert chain._monzo(x + y) == chain._monzo(x) + chain._monzo(y)
    assert chain._steps(x + y) == chain._steps(x) + chain._steps(y)
    assert chain._locate(Monzo.of(5)) is None


@given(chains, intervals)
def test_inversion_and_alteration(chain, interval):
    assert interval + chain.invert(interval) == ChainInterval(0, 1)
    assert chain.invert(chain.invert(interval)) == interval
    assert chain._steps(chain.alteration) == 0
    assert chain._ratio(chain.alteration) > 1
    quality = chain._quality(interval)
    changed = chain._quality(interval + chain.alteration)
    assert changed.kind == quality.kind
    assert changed.offset == quality.offset + 1


@pytest.mark.parametrize(
    ("period", "generator", "size"),
    [(1, Fraction(3, 2), 7), (2, 0, 7), (2, 1, 7), (2, Fraction(3, 2), 1)],
)
def test_invalid_values(period, generator, size):
    with pytest.raises(ValueError, match=r"period|generator|letters"):
        ChainNotation(Fraction(period), Fraction(generator), size)


@pytest.mark.parametrize("generator", [Fraction(2), Fraction(9, 8), Fraction(5, 3)])
def test_invalid_basis(generator):
    with pytest.raises(NotationError, match="basis"):
        ChainNotation(Fraction(2), generator, 7)


def test_incompatible_letter_layout():
    with pytest.raises(NotationError, match="symmetry"):
        ChainNotation(Fraction(2), Fraction(3, 2), 4)


@pytest.mark.parametrize("letter", [-1, 7])
def test_invalid_letter(letter):
    chain = ChainNotation(Fraction(2), Fraction(3, 2), 7)
    with pytest.raises(ValueError, match="letter"):
        chain._pitch(Spelling(letter, 0, 0))


def test_two_letter_quality_is_undefined():
    chain = ChainNotation(Fraction(2), Fraction(3, 2), 2)
    with pytest.raises(NotationError, match="two letters"):
        chain._quality(ChainInterval(1, 0))
