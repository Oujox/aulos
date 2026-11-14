import pytest
from hypothesis import given
from hypothesis import strategies as st

from aulos.base import CommaSymbols
from aulos.base import RepresentationError
from aulos.base import Symbols
from aulos.core.pitch import PitchClassValue as PitchClass
from aulos.core.pitch import PitchValue as Pitch
from aulos.pentatonic import Chord as OtherChord
from aulos.western.equal import Chord
from aulos.western.just import Chord as JustChord
from aulos.western.just import PitchClass as JustPitchClass


@given(st.integers(0, 6), st.integers(-3, 3), st.integers(-10, 10), st.integers(-5, 5))
def test_full_pitch_and_class_symbol_roundtrips(letter, alteration, register, count):
    notation, symbols = JustChord.notation, JustChord.symbols
    pc = PitchClass(notation, letter, alteration, ((5, count),))
    pitch = pc.at(register)
    rendered_pitch = symbols._render_pitch(pitch.spelling, pc.commas)
    rendered_class = symbols._render_class(pc.letter, pc.alteration, pc.commas)
    assert Pitch.of(notation, *symbols._parse_pitch(rendered_pitch)) == pitch
    assert PitchClass(notation, *symbols._parse_class(rendered_class)) == pc
    spelling, commas, suffix = symbols._split_root(rendered_class + "m7")
    assert Pitch.of(notation, spelling, commas).pitch_class == pc
    assert suffix == "m7"


@pytest.mark.parametrize("name", ["C", "C4?", "C4↑?", "C04", "C4junk"])
def test_pitch_names_reject_unconsumed_or_missing_parts(name):
    with pytest.raises(ValueError, match=r"register|comma symbol|name"):
        JustChord.symbols._parse_pitch(name)


def test_pitch_class_names_have_no_register_or_template_suffix():
    with pytest.raises(ValueError, match="unexpected"):
        Chord.symbols._parse_class("C4")
    with pytest.raises(ValueError, match="unexpected"):
        Chord.symbols._parse_class("Cm7")


def test_representation_checks_definition_and_all_required_marks():
    with pytest.raises(RepresentationError, match="letters"):
        Chord.symbols.validate(OtherChord.notation)
    with pytest.raises(RepresentationError, match="comma symbols"):
        Chord.symbols.validate(JustChord.notation)
    with pytest.raises(RepresentationError, match="alterations"):
        JustChord.symbols._render_class(0, 5, ())


def test_definitions_reject_symbols_that_cannot_write_their_notation():
    with pytest.raises(RepresentationError, match="comma symbols"):

        class Unwritable(JustPitchClass):
            symbols = Chord.symbols


@pytest.mark.parametrize(
    ("name", "register"),
    [("F4", 1), ("B4", 1), ("C4", 0), ("E4", 0), ("F-1", -4), ("C-1", -5)],
)
def test_register_labels_advance_at_the_turning_letter(name, register):
    spelling, _ = Chord.symbols._parse_pitch(name)
    assert spelling.register == register
    assert Chord.symbols._render(spelling) == name


@pytest.mark.parametrize("prime", [0, 1, 4])
def test_comma_marks_must_target_primes(prime):
    with pytest.raises(ValueError, match="prime"):
        CommaSymbols(prime, "↑", "↓")


@pytest.mark.parametrize(("raised", "lowered"), [("", "↓"), ("5", "↓"), ("↑", "-")])
def test_comma_marks_must_be_distinct_from_registers(raised, lowered):
    with pytest.raises(ValueError, match="marks"):
        CommaSymbols(5, raised, lowered)


def test_comma_mark_definitions_are_unambiguous():
    args = (Chord.symbols.letters, "#", "b", 2, 4, 4)
    mark = CommaSymbols(5, "↑", "↓")
    with pytest.raises(ValueError, match="unique"):
        Symbols(*args, (mark, mark))
    with pytest.raises(ValueError, match="place"):
        Symbols(*args, (CommaSymbols(5, "↑", "↑↑"),))
    with pytest.raises(TypeError, match="CommaSymbols"):
        Symbols(*args, (0,))  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="primes"):
        CommaSymbols(5.0, "↑", "↓")  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="strings"):
        CommaSymbols(5, 0, "↓")  # ty: ignore[invalid-argument-type]


def test_root_commas_are_carried_through_the_whole_chord():
    chord = JustChord("C↑m7")
    assert JustChord(str(chord)) == chord
    assert all(member.pitch_class.commas for member in chord.members)
    assert tuple(type(chord.root)(name) for name in chord.names) == chord.members
