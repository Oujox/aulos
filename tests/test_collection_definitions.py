from abc import ABC
from abc import abstractmethod
from fractions import Fraction

import pytest

from aulos.base import ChainInterval
from aulos.base import Chord as BaseChord
from aulos.base import NotationError
from aulos.base import NotationTag
from aulos.base import Realization
from aulos.base import RepresentationError
from aulos.base import Scale as BaseScale
from aulos.base import Template
from aulos.base import Templates
from aulos.pentatonic import Chord as OtherChord
from aulos.pentatonic import PentatonicTag
from aulos.western import WesternTag
from aulos.western.equal import Chord
from aulos.western.equal import Scale
from aulos.western.just import Chord as JustChord


def test_abstract_intermediate_classes_allow_incomplete_definitions():
    class Middle(BaseChord[WesternTag], abstract=True):
        pass

    class Concrete(Middle):
        pitch_type = Chord.pitch_type
        notation = Chord.notation
        symbols = Chord.symbols
        templates = Chord.templates
        tag = WesternTag

    assert Concrete("C").members == Chord("C").members
    with pytest.raises(TypeError, match="abstract"):
        Middle("C")
    with pytest.raises(TypeError, match="notation"):
        type("MissingDefinition", (Middle,), {})


def test_python_abstract_methods_allow_intermediate_classes():
    class AbstractChord(BaseChord[WesternTag], ABC):
        @abstractmethod
        def purpose(self):
            pass

    class Concrete(AbstractChord):
        pitch_type = Chord.pitch_type
        notation = Chord.notation
        symbols = Chord.symbols
        templates = Chord.templates
        tag = WesternTag

        def purpose(self):
            return "custom"

    assert Concrete("C").purpose() == "custom"
    with pytest.raises(TypeError, match="abstract"):
        AbstractChord("C")  # ty: ignore[call-non-callable]


@pytest.mark.parametrize("attribute", ["notation", "symbols", "templates", "realization", "tag"])
def test_concrete_classes_reject_wrong_definition_types(attribute):
    with pytest.raises(TypeError, match=attribute):
        type("Invalid", (Chord,), {attribute: object()})


@pytest.mark.parametrize("base", [BaseChord, BaseScale])
@pytest.mark.parametrize("policy", [{}, {"tag": None}, {"tag": NotationTag}])
def test_concrete_classes_require_a_validation_policy(base, policy):
    definition = {"notation": Chord.notation, "symbols": Chord.symbols, "templates": Chord.templates, **policy}
    with pytest.raises(TypeError, match="tag"):
        type("MissingPolicy", (base,), definition)


def test_symbols_tags_and_realization_are_checked_at_class_creation():
    with pytest.raises(RepresentationError, match="letters"):
        type("WrongSymbols", (Chord,), {"symbols": OtherChord.symbols})
    with pytest.raises(RepresentationError, match="comma symbols"):
        type("MissingCommas", (JustChord,), {"symbols": Chord.symbols})
    with pytest.raises(NotationError, match="western"):
        type("WrongTag", (OtherChord,), {"tag": WesternTag})
    with pytest.raises(NotationError, match="pentatonic"):
        type("WrongTag", (Chord,), {"tag": PentatonicTag})
    with pytest.raises(NotationError, match="spelling"):
        type("WrongRealization", (Chord,), {"realization": Realization(((ChainInterval(1, 0), Fraction(4, 3)),))})


@pytest.mark.parametrize("name", ["#5", "b5"])
def test_chord_templates_cannot_conflict_with_root_marks(name):
    entries = Templates((Template(name, Chord.templates.get("").intervals),))
    with pytest.raises(RepresentationError, match="template name"):
        type("AmbiguousChord", (Chord,), {"templates": entries})


@pytest.mark.parametrize("name", ["", " major", "major "])
def test_scale_names_must_be_canonical(name):
    entries = Templates((Template(name, Scale.templates.get("major").intervals),))
    with pytest.raises(ValueError, match="template name"):
        type("BadScaleName", (Scale,), {"templates": entries})


@pytest.mark.parametrize(
    ("chord_type", "error"), [(int, TypeError), (BaseChord, TypeError), (OtherChord, NotationError)]
)
def test_scale_chord_defaults_are_checked_at_definition(chord_type, error):
    with pytest.raises(error):
        type("BadScale", (Scale,), {"chord_type": chord_type})


def test_explicit_chord_class_is_required_without_a_default():
    class StandaloneScale(BaseScale[WesternTag]):
        pitch_type = Scale.pitch_type
        notation = Scale.notation
        symbols = Scale.symbols
        templates = Scale.templates
        tag = WesternTag

    scale = StandaloneScale("C major")
    with pytest.raises(TypeError, match="chord_type"):
        scale.chord()


@pytest.mark.parametrize("intervals", [(), (ChainInterval(1, 0),), (ChainInterval(0, 0), ChainInterval(0, 0))])
def test_bad_template_structures_fail_before_instantiation(intervals):
    with pytest.raises(NotationError):
        type("BadTemplate", (Chord,), {"templates": Templates((Template("bad", intervals),))})


def test_templates_and_realizations_copy_input_and_reject_ambiguity():
    values = [ChainInterval(0, 0)]
    template = Template("", values)  # ty: ignore[invalid-argument-type]
    entries = [template]
    templates = Templates(entries)  # ty: ignore[invalid-argument-type]
    values.clear()
    entries.clear()
    assert len(templates.entries[0].intervals) == 1
    assert templates.get("") == template
    with pytest.raises(ValueError, match="unknown"):
        templates.get("unknown")
    with pytest.raises(ValueError, match="unique"):
        Templates((template, template))
    with pytest.raises(ValueError, match="unique"):
        Templates((template, Template("other", (ChainInterval(0, 0),), ("",))))
    with pytest.raises(TypeError, match="string"):
        Template("", (), (0,))  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="string"):
        Template(0, ())  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="chain intervals"):
        Template("", (0,))  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="Template objects"):
        Templates((0,))  # ty: ignore[invalid-argument-type]
    with pytest.raises(ValueError, match="repeat"):
        Realization(((ChainInterval(0, 0), Fraction(1)), (ChainInterval(0, 0), Fraction(1))))
    with pytest.raises(ValueError, match="positive"):
        Realization(((ChainInterval(0, 0), Fraction(0)),))
    with pytest.raises(TypeError, match="rational"):
        Realization(((ChainInterval(0, 0), 1.5),))  # ty: ignore[invalid-argument-type]


@pytest.mark.parametrize("slash", ["", "#", "b", "C", "m"])
def test_chord_slash_cannot_conflict_with_symbols_or_templates(slash):
    with pytest.raises(RepresentationError, match="slash"):
        type("Invalid", (Chord,), {"slash": slash})
    with pytest.raises(TypeError, match="slash"):
        type("Invalid", (Chord,), {"slash": None})
    over = type("Over", (Chord,), {"slash": " over "})
    assert str(over("C over E")) == "C over E"
    assert over("C over E") == Chord("C/E")


def test_aliases_are_read_but_never_displayed():
    aliases = ["M7"]
    template = Template("maj7", Chord.templates.get("maj7").intervals, aliases)  # ty: ignore[invalid-argument-type]
    aliases.clear()
    assert template.spellings == ("maj7", "M7")
    templates = Templates((template,))
    assert templates.names == ("maj7",)
    assert templates.get("M7") is templates.get("maj7")
    assert str(Chord("CM7")) == "Cmaj7"
    assert str(Scale("A aeolian")) == "A minor"
    assert Chord("C-7/Bb") == Chord("Cm7/Bb")


@pytest.mark.parametrize("alias", ["#5", "b5", "a/b"])
def test_chord_aliases_cannot_conflict_with_root_marks_or_the_slash(alias):
    entries = Templates((Template("x", Chord.templates.get("").intervals, (alias,)),))
    with pytest.raises(RepresentationError):
        type("AmbiguousChord", (Chord,), {"templates": entries})


@pytest.mark.parametrize("alias", ["", " major", "major "])
def test_scale_aliases_follow_the_name_rules(alias):
    entries = Templates((Template("major", Scale.templates.get("major").intervals, (alias,)),))
    with pytest.raises(ValueError, match="whitespace"):
        type("BadScaleAlias", (Scale,), {"templates": entries})


def test_modes_of_the_minor_scales_are_named():
    harmonic = [str(Scale("C harmonic minor").mode(index)) for index in range(7)]
    assert harmonic == [
        "C harmonic minor",
        "D locrian #6",
        "Eb ionian #5",
        "F dorian #4",
        "G phrygian dominant",
        "Ab lydian #2",
        "B ultralocrian",
    ]
    melodic = [str(Scale("C melodic minor").mode(index)) for index in range(7)]
    assert melodic == [
        "C melodic minor",
        "D dorian b2",
        "Eb lydian augmented",
        "F lydian dominant",
        "G mixolydian b6",
        "A locrian #2",
        "B altered",
    ]


def test_altered_tensions_are_spelled_by_degree():
    assert Chord("C7#9").names == ("C4", "E4", "G4", "Bb4", "D#5")
    assert Chord("C7b9b13").names == ("C4", "E4", "G4", "Bb4", "Db5", "Ab5")
    assert Chord("C13#11").names == ("C4", "E4", "G4", "Bb4", "D5", "F#5", "A5")
