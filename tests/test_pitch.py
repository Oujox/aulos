from dataclasses import FrozenInstanceError
from fractions import Fraction

import pytest
from hypothesis import given
from hypothesis import strategies as st

from aulos.base import ChainInterval
from aulos.base import ChainNotation
from aulos.base import Comma
from aulos.base import Interval
from aulos.base import Notation
from aulos.base import NotationError
from aulos.base import Temperament
from aulos.base import TemperamentError
from aulos.base import Tuning
from aulos.core.chain import Spelling
from aulos.core.pitch import PitchClassValue as PitchClass
from aulos.core.pitch import PitchValue as Pitch

chains = [
    ChainNotation(Fraction(2), generator, size)
    for generator, size in [(Fraction(3, 2), 7), (Fraction(3, 2), 5), (Fraction(4, 3), 7), (Fraction(2, 3), 7)]
]
notations = st.sampled_from(
    [
        Notation(chain, commas)
        for chain in chains
        for commas in [(), (Comma(5, Fraction(81, 80)), Comma(7, Fraction(63, 64)))]
    ]
)
coordinates = st.integers(-8, 8)


@st.composite
def translations(draw):
    notation = draw(notations)
    counts = tuple((comma.prime, draw(coordinates)) for comma in notation.commas)
    interval = Interval(notation, ChainInterval(draw(coordinates), draw(coordinates)), counts)
    spelling = Spelling(draw(st.integers(0, notation.chain.size - 1)), draw(coordinates), draw(coordinates))
    pitch = Pitch.of(notation, spelling, counts)
    return pitch, interval


@given(translations(), coordinates)
def test_pitch_is_an_affine_space(pair, periods):
    pitch, interval = pair
    other = Interval(pitch.notation, ChainInterval(0, periods))
    zero = pitch.notation.interval(1)
    assert pitch + zero == pitch
    assert (pitch + interval) - pitch == interval
    assert (pitch + interval) - interval == pitch
    assert pitch + (interval + other) == (pitch + interval) + other
    assert (pitch + interval).ratio() == pitch.ratio() * interval.ratio()
    assert Pitch.of(pitch.notation, pitch.spelling, pitch.pitch_class.commas) == pitch


@given(translations(), coordinates)
def test_pitch_class_is_the_quotient_by_register(pair, periods):
    pitch, interval = pair
    period = Interval(pitch.notation, ChainInterval(0, periods))
    assert (pitch + period).pitch_class == pitch.pitch_class
    assert (pitch.pitch_class + interval) == (pitch + interval).pitch_class
    assert pitch.pitch_class + (interval + period) == pitch.pitch_class + interval
    assert pitch.pitch_class.at(pitch.register) == pitch
    assert (pitch.pitch_class + interval) + (-interval) == pitch.pitch_class
    assert (pitch.pitch_class + interval) - interval == pitch.pitch_class


@given(translations())
def test_interval_group_and_notation_inverse(pair):
    _, interval = pair
    notation = interval.notation
    zero = notation.interval(1)
    assert interval + (-interval) == zero
    assert interval - interval == zero
    inverse = -interval
    assert -inverse == interval
    assert notation.interval(interval.ratio()) == interval


@given(notations, coordinates, coordinates, coordinates, coordinates)
def test_interval_addition_is_commutative_and_associative(notation, a, b, c, d):
    x = Interval(notation, ChainInterval(a, b))
    y = Interval(notation, ChainInterval(c, d))
    z = notation.interval(notation.chain.period)
    assert x + y == y + x
    assert (x + y) + z == x + (y + z)
    assert (x + y).ratio() == x.ratio() * y.ratio()


@given(translations())
def test_tuning_is_external_and_linear(pair):
    pitch, interval = pair
    mapping = Temperament.equal_division((2, 3, 5, 7), 19, Fraction(2))
    tuning = Tuning(mapping, (1200 / 19,))
    assert interval.cents(tuning) == pytest.approx(tuning.cents(interval.ratio()))
    assert tuning.cents((pitch + interval).ratio()) == pytest.approx(
        tuning.cents(pitch.ratio()) + interval.cents(tuning)
    )
    assert tuning.frequency(interval.ratio(), 100) == pytest.approx(100 * 2 ** (interval.cents(tuning) / 1200))


def test_definition_equality_not_identity_or_type_parameter():
    class Category:
        pass

    left = Notation[Category](chains[0])
    equal = Notation[Category](ChainNotation(Fraction(2), Fraction(3, 2), 7))
    unequal = Notation[Category](chains[1])
    pitch = PitchClass(left, 0).at(0)
    assert pitch + equal.interval(1) == pitch
    with pytest.raises(NotationError, match="definitions"):
        pitch + unequal.interval(1)
    with pytest.raises(NotationError, match="definitions"):
        pitch - PitchClass(unequal, 0).at(0)
    with pytest.raises(NotationError, match="definitions"):
        pitch.pitch_class + unequal.interval(1)
    comma = Comma(5, Fraction(81, 80))
    with pytest.raises(NotationError):
        pitch + Notation(chains[0], (comma,)).interval(1)


def test_comma_counts_have_a_unique_immutable_normal_form():
    notation = Notation(chains[0], (Comma(5, Fraction(81, 80)),))
    pitch_class = PitchClass(notation, 0, commas=((5, 2), (5, -1)))
    assert pitch_class.commas == ((5, 1),)
    assert PitchClass(notation, 0, commas=((5, 1), (5, -1))).commas == ()
    assert Interval(notation, ChainInterval(0, 0), ((5, 2), (5, -1))).commas == ((5, 1),)
    assert hash(pitch_class) == hash(PitchClass(notation, 0, commas=((5, 1),)))
    with pytest.raises(FrozenInstanceError):
        pitch_class.letter = 1  # ty: ignore[invalid-assignment]


def test_comma_definition_order_does_not_change_the_notation():
    definitions = [Comma(5, Fraction(81, 80)), Comma(7, Fraction(63, 64))]
    notation = Notation(chains[0], definitions)  # ty: ignore[invalid-argument-type]
    assert notation == Notation(chains[0], tuple(reversed(definitions)))
    definitions.clear()
    assert len(notation.commas) == 2


@pytest.mark.parametrize("ratio", [Fraction(1, 5), Fraction(5)])
def test_both_comma_orientations_are_reversible(ratio):
    notation = Notation(chains[0], (Comma(5, ratio),))
    assert notation.interval(Fraction(25, 24)).ratio() == Fraction(25, 24)


@pytest.mark.parametrize("prime", [0, 1, 4, -5])
def test_comma_targets_must_be_prime(prime):
    with pytest.raises(ValueError, match="prime"):
        Comma(prime, 1)


@pytest.mark.parametrize(("prime", "ratio"), [(5, 1), (5, 25)])
def test_comma_target_exponent_must_be_a_unit(prime, ratio):
    with pytest.raises(NotationError, match="exactly once"):
        Comma(prime, ratio)


@pytest.mark.parametrize(
    "definitions",
    [
        (Comma(3, 3),),
        (Comma(5, Fraction(5, 7)),),
        (Comma(5, 5), Comma(5, Fraction(5, 2))),
    ],
)
def test_comma_definitions_must_be_independent(definitions):
    with pytest.raises(NotationError):
        Notation(chains[0], definitions)


@pytest.mark.parametrize("counts", [((7, 0),), ((7, 1),)])
def test_unknown_comma_is_rejected_even_with_zero_count(counts):
    notation = Notation(chains[0])
    with pytest.raises(NotationError, match="no comma"):
        PitchClass(notation, 0, commas=counts)


def test_unmapped_primes_are_distinct_from_unwritten_primes():
    notation = Notation(chains[0], (Comma(5, Fraction(81, 80)),))
    with pytest.raises(NotationError, match="prime"):
        notation.interval(7)
    with pytest.raises(TemperamentError, match="not mapped"):
        notation.interval(5).cents(Tuning(Temperament((2, 3), ((12, 19),)), (100,)))


@pytest.mark.parametrize("ratio", [0, -1])
def test_nonpositive_intervals(ratio):
    with pytest.raises(ValueError, match="positive"):
        Notation(chains[0]).interval(ratio)


@pytest.mark.parametrize("letter", [-1, 7])
def test_letter_range(letter):
    with pytest.raises(ValueError, match="letter"):
        PitchClass(Notation(chains[0]), letter)


@pytest.mark.parametrize(
    "make",
    [
        lambda: Comma(5.0, 5),  # ty: ignore[invalid-argument-type]
        lambda: Comma(5, "5"),  # ty: ignore[invalid-argument-type]
        lambda: Notation(None),  # ty: ignore[invalid-argument-type]
        lambda: Notation(chains[0], (5,)),  # ty: ignore[invalid-argument-type]
        lambda: PitchClass(Notation(chains[0]), 0.0),  # ty: ignore[invalid-argument-type]
        lambda: PitchClass(Notation(chains[0]), 0, 1.5),  # ty: ignore[invalid-argument-type]
        lambda: PitchClass(Notation(chains[0]), 0, commas=((5, 1.5),)),  # ty: ignore[invalid-argument-type]
        lambda: Interval(Notation(chains[0]), ChainInterval(0.5, 0)),  # ty: ignore[invalid-argument-type]
        lambda: Interval(Notation(chains[0]), None),  # ty: ignore[invalid-argument-type]
        lambda: Pitch(PitchClass(Notation(chains[0]), 0), 0.5),  # ty: ignore[invalid-argument-type]
    ],
)
def test_structural_input_types(make):
    with pytest.raises(TypeError):
        make()


@pytest.mark.parametrize(
    "operation",
    [
        lambda pitch, _interval: pitch + 1,
        lambda pitch, _interval: pitch - 1,
        lambda pitch, _interval: pitch + pitch,
        lambda pitch, _interval: pitch.pitch_class + 1,
        lambda pitch, _interval: pitch.pitch_class - 1,
        lambda _pitch, interval: interval + 1,
        lambda _pitch, interval: interval - 1,
    ],
)
def test_invalid_arithmetic_operands(operation):
    notation = Notation(chains[0])
    with pytest.raises(TypeError):
        operation(PitchClass(notation, 0).at(0), notation.interval(1))


def test_interval_operations_preserve_concrete_subclasses():
    class CustomInterval(Interval):
        pass

    interval = CustomInterval(Notation(chains[0]), ChainInterval(1, 0))
    assert type(interval + interval) is CustomInterval
    assert type(-interval) is CustomInterval


def test_equal_division_class_api():
    temperament = Temperament.equal_division((2, 3), 12, Fraction(2))
    between, alteration = temperament.letter_steps(chains[0])
    assert sum(between) == 12
    assert alteration > 0
    for pitch in temperament._spellings(chains[0], 1, 2):
        assert temperament.map(chains[0]._ratio(pitch)) == (1,)
