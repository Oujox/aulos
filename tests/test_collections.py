from fractions import Fraction

import pytest
from hypothesis import given
from hypothesis import strategies as st

from aulos.base import ChainInterval
from aulos.base import Chord as BaseChord
from aulos.base import Interval
from aulos.base import NotationError
from aulos.base import RepresentationError
from aulos.base import Scale as BaseScale
from aulos.base import Temperament
from aulos.base import Tuning
from aulos.pentatonic import Chord as PentatonicChord
from aulos.pentatonic import Scale as PentatonicScale
from aulos.western.equal import Chord
from aulos.western.equal import Scale
from aulos.western.just import Chord as JustChord
from aulos.western.just import Scale as JustScale

chord_types = (Chord, JustChord, PentatonicChord)
scale_types = (Scale, JustScale, PentatonicScale)
collection_types = (*chord_types, *scale_types)


@st.composite
def collections(draw, types=collection_types):
    cls = draw(st.sampled_from(types))
    template = draw(st.sampled_from(cls.templates.entries))
    letter = draw(st.sampled_from(cls.symbols.letters))
    separator = " " if issubclass(cls, BaseScale) else ""
    return cls(letter + separator + template.name)


@given(collections(), st.integers(-4, 4), st.integers(-3, 3))
def test_transposition_is_reversible_linear_and_preserves_type(collection, generators, periods):
    interval = Interval(collection.notation, ChainInterval(generators, periods))
    moved = collection.transpose(interval)
    assert type(moved) is type(collection)
    assert moved.intervals == collection.intervals
    assert moved.transpose(-interval) == collection
    assert moved.members == tuple(member + interval for member in collection.members)
    assert type(collection).from_members(collection.members) == collection
    assert type(collection).from_intervals(collection.root, iter(collection.intervals)) == collection
    assert type(collection)(str(collection)) == collection
    assert tuple(type(collection.root)(name) for name in collection.names) == collection.members
    assert hash(collection) == hash(type(collection).from_members(collection.members))


@given(collections())
def test_interval_subclasses_preserve_members_and_registered_structure(collection):
    class CustomInterval(Interval):
        pass

    intervals = tuple(CustomInterval(value.notation, value.chain, value.commas) for value in collection.intervals)
    restored = type(collection).from_intervals(collection.root, intervals)
    assert restored.intervals == intervals
    assert restored.members == collection.members
    assert restored.template_name == collection.template_name
    assert str(restored) == str(collection)
    assert restored.transpose(intervals[-1]).members == collection.transpose(collection.intervals[-1]).members


@given(collections(types=scale_types), st.integers(-15, 15), st.integers(-15, 15))
def test_modes_form_a_rotation_action(scale, first, second):
    assert scale.tonic == scale.degree(0)
    assert scale.degrees == scale.intervals
    assert scale.mode(0) == scale
    assert scale.mode(first).mode(second) == scale.mode(first + second)
    assert scale.mode(first).mode(-first) == scale
    assert type(scale.mode(first)) is type(scale)
    assert scale.mode(first).tonic == scale.degree(first)
    period = Interval(scale.notation, ChainInterval(0, 1))
    assert scale.degree(first + len(scale.degrees)) == scale.degree(first) + period


@given(collections(types=scale_types), st.integers(-8, 8), st.integers(1, 6), st.integers(1, 4))
def test_stacking_retains_exact_scale_members(scale, start, count, skip):
    chord = scale.chord(start, count, skip)
    assert type(chord) is scale.chord_type
    assert chord.members == tuple(scale.degree(start + position * skip) for position in range(count))


@given(collections(), st.integers(-5, 5))
def test_degree_lookup_ignores_only_periods(collection, periods):
    period = Interval(collection.notation, ChainInterval(0, periods))
    for member in collection.members:
        first = collection.pitch_classes.index(member.pitch_class)
        assert collection.degree_of(member + period) == first
    outside = collection.root + Interval(collection.notation, ChainInterval(700, 0))
    assert collection.degree_of(outside) is None


@given(collections())
def test_external_tuning_preserves_relative_frequency(collection):
    mapping = Temperament.equal_division((2, 3, 5), 12, Fraction(2))
    tuning = Tuning(mapping, (100.0,))
    frequencies = collection.frequencies(collection.root, 100.0, tuning)
    assert frequencies[0] == 100.0
    assert frequencies == pytest.approx(
        tuple(100 * 2 ** (interval.cents(tuning) / 1200) for interval in collection.intervals)
    )


@pytest.mark.parametrize("cls", collection_types)
def test_all_registered_templates_have_lossless_symbols(cls):
    separator = " " if issubclass(cls, BaseScale) else ""
    for template in cls.templates.entries:
        for letter in cls.symbols.letters:
            original = cls(letter + separator + template.name)
            assert cls(str(original)) == original
            assert original.template_name == template.name
            for alias in template.aliases:
                assert cls(letter + separator + alias) == original


def test_same_classification_does_not_allow_different_definitions():
    plain = Chord("Cm7")
    just = JustChord("Cm7")
    assert Chord.tag is JustChord.tag
    assert plain.pitch_classes != just.pitch_classes
    with pytest.raises(NotationError, match="definitions"):
        plain.transpose(just.intervals[1])
    with pytest.raises(NotationError, match="definitions"):
        Chord.from_members(just.members)
    with pytest.raises(NotationError, match="definitions"):
        plain.degree_of(just.root)


def test_internal_construction_and_operations_do_not_parse_strings():
    class CustomChord(Chord):
        @classmethod
        def parse_symbol(cls, symbol):
            raise AssertionError(symbol)

    class CustomScale(Scale):
        @classmethod
        def parse_symbol(cls, symbol):
            raise AssertionError(symbol)

    original = Chord("Cm7")
    custom = CustomChord.from_members(original.members)
    assert custom.members == original.members
    assert type(custom.transpose(original.intervals[1])) is CustomChord
    scale = Scale("C major")
    custom_scale = CustomScale.from_members(scale.members)
    assert type(custom_scale.mode(1)) is CustomScale
    assert type(custom_scale.chord()) is Chord


def test_unregistered_structures_have_no_invented_symbol():
    original = Chord("C")
    octave = Interval(original.notation, ChainInterval(0, 1))
    chord = Chord.from_members((original.root, original.root + octave))
    with pytest.raises(RepresentationError, match="no template"):
        str(chord)
    # 純正律のモード・和音は、元の比をテンプレートの規約で選び直さない。
    derived = JustScale("C major").chord(1)
    with pytest.raises(RepresentationError, match="no template"):
        str(derived)


@pytest.mark.parametrize("cls", [BaseChord, BaseScale])
def test_abstract_entry_points_cannot_create_instances(cls):
    with pytest.raises(TypeError, match="abstract"):
        cls("anything")
    with pytest.raises(TypeError, match="abstract"):
        cls.from_intervals(Chord("C").root, ())


@pytest.mark.parametrize(
    ("cls", "symbol"),
    [
        (Chord, ""),
        (Chord, "Qm7"),
        (Chord, "Cm7junk"),
        (Chord, "C#b"),
        (Chord, "C major"),
        (Chord, "C4m7"),
        (Scale, "C"),
        (Scale, "Cmajor"),
        (Scale, "C  major"),
        (Scale, "C major "),
        (Scale, "C unknown"),
        (PentatonicScale, "a major"),
        (PentatonicChord, "C"),
    ],
)
def test_invalid_symbols_are_not_partially_parsed(cls, symbol):
    with pytest.raises(ValueError, match=r"root|template|register|scale symbol|name"):
        cls(symbol)


@pytest.mark.parametrize(
    "intervals",
    [
        (),
        (ChainInterval(1, 0),),
        (ChainInterval(0, 0), ChainInterval(0, 0)),
        (ChainInterval(0, 0), ChainInterval(0, -1)),
    ],
)
def test_invalid_interval_order(intervals):
    notation = Chord.notation
    with pytest.raises(NotationError):
        Chord.from_intervals(Chord("C").root, (Interval(notation, interval) for interval in intervals))


def test_scale_excludes_period():
    scale = Scale("C major")
    with pytest.raises(NotationError, match="one period"):
        Scale.from_members((scale.tonic, scale.degree(7)))


@pytest.mark.parametrize("method", ["degree", "mode"])
def test_degree_indices_must_be_integers(method):
    obj = Scale("C major")
    with pytest.raises(TypeError, match="integer"):
        getattr(obj, method)(0.5)


@pytest.mark.parametrize(("count", "skip"), [(0, 2), (-1, 2), (3, 0)])
def test_stacking_requires_positive_counts(count, skip):
    with pytest.raises(ValueError, match="positive"):
        Scale("C major").chord(count=count, skip=skip)


def test_structural_type_errors():
    chord = Chord("C")
    scale = Scale("C major")
    with pytest.raises(TypeError, match="string"):
        Chord(1)  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="Pitch"):
        Chord.from_intervals(None, chord.intervals)  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="Interval"):
        Chord.from_intervals(chord.root, (1,))  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="Pitch"):
        Chord.from_members((1,))  # ty: ignore[invalid-argument-type]
    with pytest.raises(ValueError, match="member"):
        Chord.from_members(())
    with pytest.raises(TypeError, match="Interval"):
        chord.transpose(1)  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="Pitch"):
        chord.degree_of(1)  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="integer"):
        scale.chord(count=0.5)  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="integer"):
        scale.chord(degree=True)


@given(collections(chord_types), st.data())
def test_inversions_rearrange_members_without_changing_the_structure(chord, data):
    index = data.draw(st.integers(0, len(chord.intervals) - 1))
    inverted = chord.inversion(index)
    period = Interval(chord.notation, ChainInterval(0, 1))
    assert type(inverted) is type(chord)
    assert (inverted.root, inverted.intervals) == (chord.root, chord.intervals)
    assert inverted.template_name == chord.template_name
    assert inverted.bass == (chord.root + chord.intervals[index]).pitch_class
    assert inverted.members[0].pitch_class == inverted.bass
    assert chord.root.ratio() <= inverted.members[0].ratio() < (chord.root + period).ratio()
    heights = [member.ratio() for member in inverted.members]
    assert heights == sorted(set(heights))
    assert set(inverted.pitch_classes) == set(chord.pitch_classes)
    assert inverted.voicing.at(inverted.members[0]) == inverted.members
    assert type(chord)(str(inverted)) == inverted
    assert hash(type(chord)(str(inverted))) == hash(inverted)
    assert (inverted == chord) == (inverted.bass == chord.root.pitch_class)
    assert chord.inversion(0) == chord.over(chord.root.pitch_class) == chord


@given(collections(chord_types), st.data(), st.integers(-4, 4), st.integers(-3, 3))
def test_transposition_moves_the_bass_with_the_root(chord, data, generators, periods):
    inverted = chord.inversion(data.draw(st.integers(0, len(chord.intervals) - 1)))
    interval = Interval(chord.notation, ChainInterval(generators, periods))
    moved = inverted.transpose(interval)
    assert moved.bass == inverted.bass + interval
    assert moved.members == tuple(member + interval for member in inverted.members)
    assert moved.transpose(-interval) == inverted


def test_slash_chords_place_the_bass_below_the_members():
    assert Chord("C/E").names == ("E4", "G4", "C5")
    assert Chord("Cm7/Bb").names == ("Bb4", "C5", "Eb5", "G5")
    assert Chord("C/D").names == ("D4", "E4", "G4", "C5")
    assert Chord("C9/E").names == ("E4", "G4", "Bb4", "C5", "D5")
    assert str(Chord("C/C")) == "C"
    assert str(Chord("C").over(Chord("C/E").bass)) == "C/E"
    assert [str(Chord("Cmaj7").inversion(index)) for index in range(4)] == ["Cmaj7", "Cmaj7/E", "Cmaj7/G", "Cmaj7/B"]
    assert JustChord("C/E↓").names == ("E4↓", "G4", "C5")
    assert JustChord("C/E").names == ("E4", "G4", "C5", "E5↓")
    assert PentatonicChord("aopen/d").names == ("d4", "a5")
    assert Chord("C/E").degree_of(Chord("C").root) == 2
    assert Chord("C/E").root == Chord("C").root


@pytest.mark.parametrize("symbol", ["C/", "C/H", "C/E4", "C/E/G", "/E"])
def test_slash_chords_reject_malformed_basses(symbol):
    with pytest.raises(ValueError, match=r"letter|pitch class"):
        Chord(symbol)


def test_bass_and_inversion_arguments_are_checked():
    chord = Chord("C")
    with pytest.raises(TypeError, match="PitchClass"):
        chord.over("E")  # ty: ignore[invalid-argument-type]
    with pytest.raises(NotationError, match="definitions"):
        chord.over(JustChord("C").bass)
    with pytest.raises(TypeError, match="integer"):
        chord.inversion(True)  # noqa: FBT003
    with pytest.raises(ValueError, match="3 members"):
        chord.inversion(3)
    with pytest.raises(ValueError, match="3 members"):
        chord.inversion(-1)


@given(collections())
def test_structure_names_ignore_commas(collection):
    assert collection.structure_name == collection.template_name
    plain = type(collection).from_intervals(
        collection.root, (Interval(collection.notation, interval.chain) for interval in collection.intervals)
    )
    assert plain.structure_name == collection.structure_name


def test_structure_names_remain_when_ratios_leave_the_convention():
    supertonic = JustScale("C major").chord(1)
    assert [str(interval.ratio()) for interval in supertonic.intervals] == ["1", "32/27", "40/27"]
    assert supertonic.structure_name == "m"
    assert JustScale("C major").mode(1).structure_name == "dorian"
    assert Chord("C/E").structure_name == ""
    with pytest.raises(RepresentationError, match="represents"):
        _ = supertonic.template_name
    with pytest.raises(RepresentationError, match="spells"):
        _ = Chord.from_members([Chord("C").root, Chord("Db").root]).structure_name
