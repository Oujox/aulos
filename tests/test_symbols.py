import pytest
from hypothesis import given
from hypothesis import strategies as st

from aulos.core.chain import Spelling
from aulos.core.errors import RepresentationError
from aulos.core.symbols import Symbols


@given(st.integers(0, 2), st.integers(-2, 2), st.integers(-10, 10), st.integers(0, 2), st.integers(-5, 5))
def test_display_roundtrip(letter, alteration, register, turn, label):
    symbols = Symbols(("Do", "Re", "Mi"), "up", "down", 2, turn, label)
    spelling = Spelling(letter, alteration, register)
    name = symbols._render(spelling)
    assert symbols._parse(name) == spelling
    assert symbols._render(symbols._parse(name)) == name


@pytest.mark.parametrize(
    ("letters", "raised", "lowered", "most", "turn"),
    [
        (("",), "+", "b", 1, 0),
        (("A", "A"), "+", "b", 1, 0),
        (("A", "Ab"), "+", "b", 1, 0),
        (("A1",), "+", "b", 1, 0),
        (("A-",), "+", "b", 1, 0),
        ((), "+", "b", 1, 0),
        (("A",), "+", "b", 1, 1),
        (("A",), "+", "b", -1, 0),
    ],
)
def test_invalid_definition(letters, raised, lowered, most, turn):
    with pytest.raises(ValueError, match=r"symbol|letter|alterations"):
        Symbols(letters, raised, lowered, most, turn, 0)


@pytest.mark.parametrize("attribute", ["most", "turn", "label"])
@given(st.one_of(st.floats(), st.text(), st.booleans(), st.none()))
def test_numeric_settings_require_integers(attribute, invalid):
    values = {"most": 1, "turn": 0, "label": 0, attribute: invalid}
    with pytest.raises(TypeError, match="integers"):
        Symbols(("A",), "#", "b", values["most"], values["turn"], values["label"])


@pytest.mark.parametrize("spelling", [Spelling(-1, 0, 0), Spelling(1, 0, 0), Spelling(0, 2, 0)])
def test_unrepresentable(spelling):
    symbols = Symbols(("A",), "#", "b", 1, 0, 0)
    with pytest.raises(RepresentationError):
        symbols._render(spelling)


@pytest.mark.parametrize("name", ["", "B0", "A", "A#b0", "A##0", "A01", "A+1", "A-0", "A 1"])
def test_invalid_name(name):
    symbols = Symbols(("A",), "#", "b", 1, 0, 0)
    with pytest.raises(ValueError, match=r"letter|register|name"):
        symbols._parse(name)
