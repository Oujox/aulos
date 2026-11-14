from fractions import Fraction

import pytest

from aulos.core.chain import ChainNotation
from aulos.core.chain import Spelling
from aulos.core.errors import NotationError
from aulos.core.errors import RepresentationError
from aulos.core.errors import RhythmError
from aulos.core.errors import TemperamentError
from aulos.core.monzo import Monzo
from aulos.core.symbols import Symbols
from aulos.core.temper import Temperament
from aulos.core.temper import Tuning


def test_notation_structure_error():
    with pytest.raises(NotationError):
        ChainNotation(Fraction(2), Fraction(9, 8), 7)


def test_unsupported_temperament_prime():
    temperament = Temperament((2, 3), ((12, 19),))
    with pytest.raises(TemperamentError):
        temperament.map(5)


def test_temperament_incompatible_with_operation():
    chain = ChainNotation(Fraction(2), Fraction(3, 2), 7)
    temperament = Temperament((2, 3), ((1, 0), (0, 1)))
    with pytest.raises(TemperamentError):
        temperament.letter_steps(chain)


def test_unrepresentable_spelling():
    symbols = Symbols(("C", "D", "E", "F", "G", "A", "B"), "#", "b", 1, 0, 4)
    with pytest.raises(RepresentationError):
        symbols._render(Spelling(0, 2, 0))


@pytest.mark.parametrize("error", [NotationError, TemperamentError, RepresentationError, RhythmError])
def test_domain_errors_can_be_caught_as_value_errors(error):
    assert issubclass(error, ValueError)


def test_invalid_values_use_builtin_error():
    with pytest.raises(ValueError, match="not a positive ratio") as raised:
        Monzo.of(0)
    assert type(raised.value) is ValueError

    with pytest.raises(ValueError, match="not above 1") as raised:
        ChainNotation(Fraction(1), Fraction(3, 2), 7)
    assert type(raised.value) is ValueError

    with pytest.raises(ValueError, match="one count per prime") as raised:
        Temperament((2, 3), ((12,),))
    assert type(raised.value) is ValueError

    with pytest.raises(ValueError, match="finite size") as raised:
        Tuning(Temperament((2,), ((12,),)), (float("inf"),))
    assert type(raised.value) is ValueError

    symbols = Symbols(("C",), "#", "b", 1, 0, 4)
    with pytest.raises(ValueError, match="does not start with a letter") as raised:
        symbols._parse("invalid")
    assert type(raised.value) is ValueError


def test_invalid_type_uses_builtin_error():
    with pytest.raises(TypeError):
        Monzo.of(object())  # ty: ignore[invalid-argument-type]
