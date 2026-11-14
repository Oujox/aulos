import inspect
import re
from dataclasses import FrozenInstanceError
from fractions import Fraction
from math import log2

import pytest
from hypothesis import given
from hypothesis import strategies as st

import aulos.base
from aulos import core
from aulos.base import ChainInterval
from aulos.base import Chord as BaseChord
from aulos.base import Interval
from aulos.base import NotationError
from aulos.base import Pitch as BasePitch
from aulos.base import PitchClass as BasePitchClass
from aulos.base import RepresentationError
from aulos.base import Symbols
from aulos.base import Temperament
from aulos.base import TemperamentError
from aulos.base import Tuning
from aulos.base import Voicing as BaseVoicing
from aulos.pentatonic import Chord as PentatonicChord
from aulos.pentatonic import Pitch as PentatonicPitch
from aulos.pentatonic import PitchClass as PentatonicPitchClass
from aulos.western import WesternTag
from aulos.western import equal
from aulos.western import just
from aulos.western import letters

PRIVATE_TYPES = re.compile(r"\b(Monzo|Spelling|ChainPitch|PitchValue|PitchClassValue)\b")
systems = (equal, just)


@st.composite
def pitches(draw):
    module = draw(st.sampled_from(systems))
    letter = draw(st.integers(0, 6))
    alteration = draw(st.integers(-3, 3))
    register = draw(st.integers(-4, 4))
    commas = ((5, draw(st.integers(-3, 3))),) if module is just else ()
    return module.Pitch.from_class(module.PitchClass.from_spelling(letter, alteration, commas), register)


def test_core_has_no_public_names():
    assert not hasattr(core, "__all__")
    assert all(inspect.ismodule(value) for name, value in vars(core).items() if not name.startswith("_"))


def test_public_names_are_classes_and_exclude_private_types():
    assert all(inspect.isclass(getattr(aulos.base, name)) for name in aulos.base.__all__)
    assert not {"Monzo", "Spelling", "ChainPitch"} & set(aulos.base.__all__)


@pytest.mark.parametrize("name", aulos.base.__all__)
def test_public_members_do_not_expose_private_types(name):
    cls = getattr(aulos.base, name)
    for attribute, value in vars(cls).items():
        if attribute.startswith("_") and attribute != "__init__":
            continue
        target = value.__func__ if isinstance(value, (classmethod, staticmethod)) else value
        target = target.fget if isinstance(target, property) else target
        if inspect.isfunction(target):
            assert not PRIVATE_TYPES.search(str(inspect.signature(target))), f"{name}.{attribute}"
    for attribute, annotation in inspect.get_annotations(cls).items():
        if not attribute.startswith("_"):
            assert not PRIVATE_TYPES.search(str(annotation)), f"{name}.{attribute}"


@pytest.mark.parametrize("module", systems)
def test_names_round_trip_and_keep_concrete_types(module):
    pitch = module.Pitch("C#4")
    assert str(pitch) == "C#4"
    assert module.Pitch(str(pitch)) == pitch
    assert type(pitch.pitch_class) is module.PitchClass
    assert pitch.pitch_class == module.PitchClass("C#")
    assert str(pitch.pitch_class) == "C#"
    assert module.Pitch.from_class(pitch.pitch_class, pitch.register) == pitch


@given(pitches(), st.integers(-6, 6), st.integers(-6, 6))
def test_pitch_is_an_affine_space_over_intervals(pitch, generators, periods):
    interval = Interval(pitch.notation, ChainInterval(generators, periods))
    moved = pitch + interval
    assert type(moved) is type(pitch)
    assert moved - pitch == interval
    assert moved - interval == pitch
    assert moved.ratio() == pitch.ratio() * interval.ratio()
    assert pitch.pitch_class + interval == moved.pitch_class
    assert moved.pitch_class - interval == pitch.pitch_class
    assert hash(type(pitch).from_class(pitch.pitch_class, pitch.register)) == hash(pitch)


def test_pitch_class_ignores_the_register_but_not_the_spelling():
    assert equal.Pitch("C4").pitch_class == equal.Pitch("C5").pitch_class
    assert equal.Pitch("C4") != equal.Pitch("C5")
    assert equal.PitchClass("C#") != equal.PitchClass("Db")
    assert just.PitchClass("A") != just.PitchClass("A↓")
    assert equal.Pitch("C4").register + 1 == equal.Pitch("C5").register


def test_comma_fields_are_public_on_the_pitch_class():
    pitch_class = just.PitchClass("A↓")
    assert (pitch_class.letter, pitch_class.alteration, pitch_class.commas) == (2, 0, ((5, -1),))


def test_subclasses_are_preserved_by_arithmetic():
    class CustomPitch(equal.Pitch):
        pass

    class CustomPitchClass(equal.PitchClass):
        pass

    interval = equal.notation.interval(Fraction(3, 2))
    assert type(CustomPitch("C4") + interval) is CustomPitch
    assert type(CustomPitch("C4") - interval) is CustomPitch
    assert type(CustomPitchClass("C") + interval) is CustomPitchClass


def test_pitches_are_immutable_and_compared_by_notated_value():
    pitch = equal.Pitch("C4")
    with pytest.raises(FrozenInstanceError):
        pitch._value = None  # ty: ignore[invalid-assignment]
    assert pitch != just.Pitch("C4")
    assert pitch != equal.PitchClass("C")


def test_equality_ignores_symbols_and_bound_tuning():
    typeset = Symbols(letters, "♯", "♭", 4, 4, 4)
    names = {"symbols": typeset, "tuning": None}
    pitch_class_type = type("PitchClass", (equal.PitchClass,), names)
    pitch_type = type("Pitch", (equal.Pitch,), {**names, "pitch_class_type": pitch_class_type})
    voicing_type = type("Voicing", (equal.Voicing,), {**names, "pitch_type": pitch_type})
    chord_type = type("Chord", (equal.Chord,), {**names, "pitch_type": pitch_type, "voicing_type": voicing_type})
    scale_type = type("Scale", (equal.Scale,), {**names, "pitch_type": pitch_type, "chord_type": chord_type})
    pairs = [
        (pitch_class_type("C♯"), equal.PitchClass("C#")),
        (pitch_type("C♯4"), equal.Pitch("C#4")),
        (voicing_type("m7"), equal.Voicing("m7")),
        (chord_type("E♭m7"), equal.Chord("Ebm7")),
        (scale_type("B♭ major"), equal.Scale("Bb major")),
    ]
    for custom, plain in pairs:
        assert custom == plain
        assert hash(custom) == hash(plain)
    assert (str(pairs[1][0]), str(pairs[1][1])) == ("C♯4", "C#4")
    assert pitch_type("C♯4") != equal.Pitch("Db4")


def test_structures_of_different_kinds_are_not_equal():
    chord = equal.Chord("C")
    scale = equal.Scale.from_intervals(chord.root, chord.intervals)
    assert scale.members == chord.members
    assert chord != scale
    assert chord.voicing != chord
    assert chord.voicing == equal.Voicing("")


@pytest.mark.parametrize("cls", [BasePitch, BasePitchClass, BaseVoicing])
def test_abstract_pitches_cannot_be_created(cls):
    with pytest.raises(TypeError, match="abstract"):
        cls("C")


@pytest.mark.parametrize(
    "make",
    [
        lambda: equal.Pitch(1),  # ty: ignore[invalid-argument-type]
        lambda: equal.PitchClass(1),  # ty: ignore[invalid-argument-type]
        lambda: equal.Voicing(1),  # ty: ignore[invalid-argument-type]
        lambda: equal.Pitch.from_class(None),  # ty: ignore[invalid-argument-type]
        lambda: equal.Pitch.from_class(equal.PitchClass("C"), 0.5),  # ty: ignore[invalid-argument-type]
        lambda: equal.PitchClass.from_spelling(0.0),  # ty: ignore[invalid-argument-type]
        lambda: equal.PitchClass.from_spelling(0, 1.5),  # ty: ignore[invalid-argument-type]
        lambda: equal.PitchClass.from_spelling(0, 0, ((5, 1.5),)),  # ty: ignore[invalid-argument-type]
        lambda: equal.Pitch("C4") + 1,  # ty: ignore[unsupported-operator]
        lambda: equal.Pitch("C4") - 1,  # ty: ignore[unsupported-operator]
        lambda: equal.Pitch("C4") + equal.Pitch("C4"),  # ty: ignore[unsupported-operator]
        lambda: equal.PitchClass("C") + 1,  # ty: ignore[unsupported-operator]
        lambda: equal.PitchClass("C") - 1,  # ty: ignore[unsupported-operator]
    ],
)
def test_structural_input_types(make):
    with pytest.raises(TypeError):
        make()


@pytest.mark.parametrize("letter", [-1, 7])
def test_letter_range(letter):
    with pytest.raises(ValueError, match="letter"):
        equal.PitchClass.from_spelling(letter)


@pytest.mark.parametrize(("cls", "name"), [(equal.Pitch, "C"), (equal.PitchClass, "C4"), (PentatonicPitch, "C4")])
def test_invalid_names(cls, name):
    with pytest.raises(ValueError, match=r"register|unexpected|letter"):
        cls(name)


def test_different_definitions_do_not_mix():
    with pytest.raises(NotationError, match="definitions"):
        equal.Pitch("C4") - just.Pitch("C4")
    with pytest.raises(NotationError, match="definitions"):
        equal.Pitch("C4") + just.notation.interval(1)
    with pytest.raises(NotationError, match="definitions"):
        equal.PitchClass("C") + just.notation.interval(1)
    with pytest.raises(NotationError, match="definitions"):
        equal.Pitch.from_class(just.PitchClass("C"))
    with pytest.raises(NotationError, match="definitions"):
        equal.Voicing("m7").at(just.Pitch("C4"))


def test_equal_temperament_is_bound():
    assert equal.Pitch("A4").frequency(equal.Pitch("A4"), 440.0) == 440.0
    assert equal.Pitch("A5").frequency(equal.Pitch("A4"), 440.0) == pytest.approx(880.0)
    sharp = equal.Pitch("C#4").frequency(equal.Pitch("A4"), 440.0)
    assert sharp == pytest.approx(equal.Pitch("Db4").frequency(equal.Pitch("A4"), 440.0))
    fifth = equal.Chord("C5").frequencies(equal.Pitch("C4"), 100.0)
    assert fifth == pytest.approx((100.0, 100 * 2 ** (700 / 1200)))


def test_just_tuning_is_bound():
    frequencies = just.Chord("Cm7").frequencies(just.Pitch("C4"), 100.0)
    assert frequencies == pytest.approx((100.0, 120.0, 150.0, 180.0))
    assert just.tuning.cents(Fraction(5, 4)) == pytest.approx(1200 * log2(Fraction(5, 4)))


def test_explicit_tuning_overrides_the_bound_one():
    meantone = Tuning(Temperament((2, 3), ((12, 19),)), (50.0,))
    assert equal.Pitch("C5").frequency(equal.Pitch("C4"), 100.0, meantone) == pytest.approx(200.0 * 2 ** (-0.5))
    assert equal.Chord("C5").frequencies(equal.Pitch("C4"), 100.0, meantone)[0] == 100.0


def test_unbound_tuning_must_be_passed():
    with pytest.raises(TypeError, match="tuning"):
        PentatonicPitch("a4").frequency(PentatonicPitch("a4"), 100.0)
    with pytest.raises(TypeError, match="tuning"):
        PentatonicChord("a").frequencies(PentatonicPitch("a4"), 100.0)
    assert PentatonicPitch("a4").frequency(PentatonicPitch("a4"), 100.0, equal.tuning) == 100.0


def test_bound_tuning_must_cover_the_notation():
    with pytest.raises(TypeError, match="tuning"):
        type("WrongTuning", (equal.Chord,), {"tuning": object()})
    two_only = Tuning(Temperament((2,), ((12,),)), (100.0,))
    with pytest.raises(TemperamentError, match="not mapped"):
        type("WrongTuning", (equal.Chord,), {"tuning": two_only})
    with pytest.raises(TemperamentError, match="not mapped"):
        type("WrongTuning", (just.Chord,), {"tuning": equal.tuning})


@pytest.mark.parametrize("size", [0.0, -100.0])
def test_bound_tuning_must_raise_the_period(size):
    falling = Tuning(equal.tuning.temperament, (size,))
    with pytest.raises(TemperamentError, match="positive size"):
        type("WrongTuning", (equal.Chord,), {"tuning": falling})
    assert equal.Chord("C").frequencies(equal.Pitch("C4"), 100.0, falling)[0] == 100.0


def test_notation_lists_the_primes_it_writes():
    assert equal.notation.primes == (2, 3)
    assert just.notation.primes == (2, 3, 5)


@pytest.mark.parametrize(
    ("attribute", "value"), [("pitch_type", int), ("voicing_type", int), ("pitch_type", BasePitch)]
)
def test_collaborator_types_are_checked(attribute, value):
    with pytest.raises(TypeError, match=attribute):
        type("Invalid", (equal.Chord,), {attribute: value})


def test_collaborators_must_share_the_notation():
    with pytest.raises(NotationError, match="definitions"):
        type("Invalid", (equal.Chord,), {"pitch_type": just.Pitch})
    with pytest.raises(NotationError, match="definitions"):
        type("Invalid", (equal.Chord,), {"voicing_type": just.Voicing})
    with pytest.raises(NotationError, match="definitions"):
        type("Invalid", (equal.Pitch,), {"pitch_class_type": just.PitchClass})
    with pytest.raises(TypeError, match="pitch_class_type"):
        type("Invalid", (equal.Pitch,), {"pitch_class_type": BasePitchClass})


@pytest.mark.parametrize("module", systems)
def test_voicing_is_the_rootless_structure_of_a_chord(module):
    chord = module.Chord("Dm7")
    voicing = chord.voicing
    assert type(voicing) is module.Voicing
    assert voicing == module.Voicing("m7")
    assert voicing.intervals == chord.intervals
    assert str(voicing) == voicing.template_name == "m7"
    assert voicing.at(chord.root) == chord.members
    assert module.Chord.from_intervals(chord.root, voicing.intervals) == chord
    assert hash(voicing) == hash(module.Voicing.from_intervals(voicing.intervals))


def test_voicing_does_not_depend_on_the_root():
    assert equal.Chord("Cm7").voicing == equal.Chord("F#m7").voicing
    assert [str(pitch) for pitch in equal.Voicing("m7").at(equal.Pitch("D4"))] == ["D4", "F4", "A4", "C5"]


def test_voicing_may_span_periods_and_double_pitch_classes():
    octave = Interval(equal.notation, ChainInterval(0, 1))
    third = equal.Voicing("").intervals[1]
    voicing = equal.Voicing.from_intervals((equal.notation.interval(1), third, octave, octave + third))
    pitches_ = voicing.at(equal.Pitch("C4"))
    assert [str(pitch) for pitch in pitches_] == ["C4", "E4", "C5", "E5"]
    assert pitches_[0].pitch_class == pitches_[2].pitch_class
    with pytest.raises(RepresentationError, match="no template"):
        str(voicing)


@pytest.mark.parametrize(
    "intervals",
    [
        (),
        (ChainInterval(1, 0),),
        (ChainInterval(0, 0), ChainInterval(0, 0)),
        (ChainInterval(0, 0), ChainInterval(0, -1)),
    ],
)
def test_voicing_order_is_validated(intervals):
    with pytest.raises(NotationError):
        equal.Voicing.from_intervals(Interval(equal.notation, interval) for interval in intervals)


def test_voicing_inputs_are_checked():
    with pytest.raises(ValueError, match="unknown"):
        equal.Voicing("nonsense")
    with pytest.raises(TypeError, match="Interval"):
        equal.Voicing.from_intervals((1,))  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="Pitch"):
        equal.Voicing("m7").at(None)  # ty: ignore[invalid-argument-type]


def test_voicing_requires_a_declared_type():
    class Bare(BaseChord[WesternTag]):
        pitch_type = equal.Pitch
        notation = equal.notation
        symbols = equal.symbols
        templates = equal.Chord.templates
        tag = WesternTag

    with pytest.raises(TypeError, match="voicing_type"):
        _ = Bare("C").voicing


def test_collections_hold_concrete_pitches():
    chord = equal.Chord("Cm7")
    assert all(type(member) is equal.Pitch for member in chord.members)
    assert all(type(pitch_class) is equal.PitchClass for pitch_class in chord.pitch_classes)
    assert chord.degree_of(equal.Pitch("G6")) == 2
    assert PentatonicChord("a").pitch_classes[0] == PentatonicPitchClass("a")


@given(pitches(), pitches())
def test_interval_steps_count_letters_and_quality_follows_alterations(low, high):
    if low.notation != high.notation:
        return
    interval = high - low
    alteration = Interval(low.notation, low.notation.chain.alteration)
    size = low.notation.chain.size
    assert interval.steps == (high.register - low.register) * size + high.pitch_class.letter - low.pitch_class.letter
    assert (-interval).steps == -interval.steps
    assert (interval + interval).steps == 2 * interval.steps
    assert (interval + alteration).steps == interval.steps
    assert (interval + alteration).quality.kind == interval.quality.kind
    assert (interval + alteration).quality.offset == interval.quality.offset + 1
    assert Interval(interval.notation, interval.chain).quality == interval.quality


def test_interval_qualities_name_western_intervals():
    def quality(low, high):
        interval = equal.Pitch(high) - equal.Pitch(low)
        return interval.steps, interval.quality.kind, interval.quality.offset

    assert quality("C4", "G4") == (4, "perfect", 0)
    assert quality("C4", "E4") == (2, "imperfect", 0)
    assert quality("C4", "Eb4") == (2, "imperfect", -1)
    assert quality("F4", "B4") == (3, "perfect", 1)
    assert quality("B3", "F4") == (4, "perfect", -1)
    assert quality("C4", "Bbb4") == (6, "imperfect", -2)
    assert quality("C4", "D5") == (8, "imperfect", 0)
    assert quality("G4", "C4") == (-4, "perfect", 0)
    assert (just.Pitch("E4↓") - just.Pitch("C4")).quality == (equal.Pitch("E4") - equal.Pitch("C4")).quality


@given(pitches(), st.integers(0, 3))
def test_enharmonics_sound_alike_and_are_spelled_apart(pitch, most):
    division = Tuning(Temperament.equal_division((2, 3, 5), 12, Fraction(2)), (100.0,))
    others = pitch.enharmonics(division, most)
    assert pitch not in others
    assert len(set(others)) == len(others)
    assert all(type(other) is type(pitch) for other in others)
    assert all(not other.pitch_class.commas and abs(other.pitch_class.alteration) <= most for other in others)
    assert all((other - pitch).cents(division) == 0.0 for other in others)
    assert [abs(other.pitch_class.alteration) for other in others] == sorted(
        abs(other.pitch_class.alteration) for other in others
    )
    if not pitch.pitch_class.commas and abs(pitch.pitch_class.alteration) <= most:
        assert all(pitch in other.enharmonics(division, most) for other in others)


def test_enharmonics_depend_on_the_tuning():
    nineteen = Tuning(Temperament.equal_division((2, 3), 19, Fraction(2)), (1200 / 19,))
    assert [str(pitch) for pitch in equal.Pitch("C#4").enharmonics(most=1)] == ["Db4"]
    assert [str(pitch) for pitch in equal.Pitch("C#4").enharmonics(most=2)] == ["Db4", "B##3"]
    assert [str(pitch) for pitch in equal.Pitch("C#4").enharmonics(nineteen, 2)] == ["Dbb4"]
    assert len(equal.Pitch("C4").enharmonics()) == len(equal.Pitch("C4").enharmonics(most=equal.symbols.most))
    with pytest.raises(TemperamentError, match="single generator"):
        just.Pitch("E4").enharmonics()
    with pytest.raises(TypeError, match="tuning"):
        PentatonicPitch("a4").enharmonics()
    with pytest.raises(TypeError, match="integer"):
        equal.Pitch("C4").enharmonics(most=1.0)  # ty: ignore[invalid-argument-type]
    with pytest.raises(ValueError, match="negative"):
        equal.Pitch("C4").enharmonics(most=-1)
