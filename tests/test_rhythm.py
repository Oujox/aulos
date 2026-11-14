import inspect
import math
from fractions import Fraction

import pytest
from hypothesis import given
from hypothesis import strategies as st

import aulos.rhythm
from aulos.rhythm import Cycle
from aulos.rhythm import Duration
from aulos.rhythm import Event
from aulos.rhythm import Meter
from aulos.rhythm import NoteValue
from aulos.rhythm import Parallel
from aulos.rhythm import Placed
from aulos.rhythm import Position
from aulos.rhythm import RhythmError
from aulos.rhythm import Serial
from aulos.rhythm import Tempo
from aulos.rhythm import TempoMap
from aulos.western.equal import Pitch

fractions = st.fractions(-8, 8, max_denominator=24)
durations = st.builds(Duration, fractions)
positions = st.builds(Position, fractions)
lengths = st.builds(Duration, st.fractions(0, 4, max_denominator=12))
factors = st.fractions(Fraction(1, 6), 6, max_denominator=6)
meters = st.builds(
    Meter,
    st.lists(st.integers(2, 4), min_size=1, max_size=3).map(tuple),
    st.sampled_from([Duration(Fraction(1, 8)), Duration(Fraction(1, 16)), Duration(Fraction(1, 12))]),
)
eighth = Duration(Fraction(1, 8))
quarter = Duration(Fraction(1, 4))


@st.composite
def cycles(draw):
    size = draw(st.integers(1, 16))
    return Cycle(size, tuple(draw(st.sets(st.integers(0, size - 1)))))


@st.composite
def parts(draw, depth=2):
    if depth == 0 or draw(st.booleans()):
        return Event(draw(lengths), draw(st.none() | st.integers(0, 9)))
    children = tuple(draw(st.lists(parts(depth=depth - 1), max_size=3)))
    return draw(st.sampled_from([Serial, Parallel]))(children)


def test_public_names_are_classes():
    assert all(inspect.isclass(getattr(aulos.rhythm, name)) for name in aulos.rhythm.__all__)
    assert aulos.rhythm.__all__ == sorted(aulos.rhythm.__all__)


@given(durations, durations, durations, st.integers(-5, 5), factors)
def test_durations_form_an_ordered_group_with_rational_scaling(x, y, z, times, factor):
    zero = Duration(0)
    assert (x + y) + z == x + (y + z)
    assert x + y == y + x
    assert x + zero == x
    assert x + (-x) == zero
    assert x - y == x + (-y)
    assert (x < y) == (x.value < y.value)
    assert (x + z < y + z) == (x < y)
    assert x * times == times * x == Duration(x.value * times)
    assert (x + y) * factor == x * factor + y * factor
    assert x * factor / factor == x
    if y != zero:
        assert y * (x / y) == x
    assert hash(Duration(x.value)) == hash(x)


@given(positions, durations, durations)
def test_positions_are_a_torsor_over_durations(position, x, y):
    assert (position + x) + y == position + (x + y)
    assert (position + x) - position == x
    assert (position + x) - x == position
    assert position + Duration(0) == position
    assert (position < position + x) == (x > Duration(0))


def test_time_values_reject_inexact_numbers_and_mixed_arithmetic():
    for cls in (Duration, Position):
        for value in (0.5, True, "1/4"):
            with pytest.raises(TypeError, match="integer or a Fraction"):
                cls(value)  # ty: ignore[invalid-argument-type]
    for operation in (
        lambda: Position(0) + Position(1),  # ty: ignore[unsupported-operator]
        lambda: Duration(1) + Position(0),  # ty: ignore[unsupported-operator]
        lambda: Duration(1) + 1,  # ty: ignore[unsupported-operator]
        lambda: Duration(1) - 1,  # ty: ignore[unsupported-operator]
        lambda: Duration(1) * 0.5,  # ty: ignore[unsupported-operator]
        lambda: Duration(1) * True,
        lambda: Duration(1) / 0.5,  # ty: ignore[unsupported-operator]
        lambda: Position(0) - 1,  # ty: ignore[unsupported-operator]
        lambda: Duration(1) < Position(1),  # ty: ignore[unsupported-operator]
    ):
        with pytest.raises(TypeError):
            operation()
    with pytest.raises(ZeroDivisionError):
        Duration(1) / Duration(0)


def test_duration_primes_name_the_subdivisions():
    assert Duration(3).primes == frozenset()
    assert Duration(Fraction(3, 8)).primes == {2}
    assert Duration(Fraction(1, 12)).primes == {2, 3}
    assert Duration(Fraction(-1, 20)).primes == {2, 5}


@given(meters, st.integers(-3, 3), st.data())
def test_meter_levels_are_a_chain_of_subgroups(meter, bar, data):
    pulse = data.draw(st.integers(0, meter.pulses - 1))
    position = meter.position(bar, pulse)
    level = meter.level(position)
    depth = len(meter.divisions)
    assert meter.locate(position) == (bar, meter.pulse * pulse)
    assert meter.bar == meter.pulse * meter.pulses == meter.unit(0)
    assert meter.unit(depth) == meter.pulse
    assert all(meter.unit(index) == meter.unit(index + 1) * meter.divisions[index] for index in range(depth))
    for index in range(depth + 1):
        on_grid = pulse % (meter.pulses // math.prod(meter.divisions[:index])) == 0
        assert on_grid == (index >= level)
    assert meter.weights[pulse] == depth - level
    assert meter.level(meter.position(bar)) == 0
    assert meter.weights.count(depth) == 1
    with pytest.raises(RhythmError, match="between the pulses"):
        meter.level(position + meter.pulse / 2)


def test_meters_with_one_bar_length_differ_by_their_levels():
    compound, simple = Meter((2, 3), eighth), Meter((3, 2), eighth)
    assert compound.bar == simple.bar == Duration(Fraction(3, 4))
    assert compound.weights == (2, 0, 0, 1, 0, 0)
    assert simple.weights == (2, 0, 1, 0, 1, 0)
    assert Meter((2, 2, 2), eighth).weights == (3, 0, 1, 0, 2, 0, 1, 0)
    assert Meter((2, 2), quarter).locate(Position(Fraction(-1, 4))) == (-1, Duration(Fraction(3, 4)))


@pytest.mark.parametrize(
    ("divisions", "pulse", "error"),
    [
        ((), eighth, ValueError),
        ((2, 1), eighth, ValueError),
        ((2,), Duration(0), ValueError),
        ((2,), -eighth, ValueError),
        ((2.0,), eighth, TypeError),
        ((True,), eighth, TypeError),
        ((2,), Fraction(1, 8), TypeError),
    ],
)
def test_invalid_meters(divisions, pulse, error):
    with pytest.raises(error, match=r"divisions|pulse"):
        Meter(divisions, pulse)


def test_meter_arguments_are_checked():
    meter = Meter((2, 2), quarter)
    with pytest.raises(ValueError, match="levels 0 to 2"):
        meter.unit(3)
    with pytest.raises(TypeError, match="level"):
        meter.unit(1.0)  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="integers"):
        meter.position(0.5)  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="Position"):
        meter.locate(Duration(1))  # ty: ignore[invalid-argument-type]


@given(cycles(), st.integers(-20, 20), st.integers(-20, 20), st.integers(1, 4))
def test_rotation_is_a_cyclic_group_action(cycle, x, y, factor):
    assert cycle.rotate(0) == cycle.rotate(cycle.size) == cycle
    assert cycle.rotate(x).rotate(y) == cycle.rotate(x + y)
    assert sum(cycle.steps) == (cycle.size if cycle.onsets else 0)
    assert sorted(cycle.rotate(x).steps) == sorted(cycle.steps)
    assert cycle.complement().complement() == cycle
    assert not (cycle & cycle.complement()).onsets
    assert (cycle | cycle.complement()).onsets == tuple(range(cycle.size))
    assert cycle.refine(factor).steps == tuple(step * factor for step in cycle.steps)
    assert cycle.repeat(factor).steps == cycle.steps * factor
    assert cycle.durations(eighth) == tuple(eighth * step for step in cycle.steps)
    assert hash(Cycle(cycle.size, cycle.onsets[::-1] * 2)) == hash(cycle)


@given(cycles(), st.data())
def test_modes_start_from_each_onset(cycle, data):
    if not cycle.onsets:
        with pytest.raises(RhythmError, match="no mode"):
            cycle.mode(0)
        return
    index = data.draw(st.integers(-8, 8))
    mode = cycle.mode(index)
    turn = index % len(cycle.onsets)
    assert mode.onsets[0] == 0
    assert mode.steps == cycle.steps[turn:] + cycle.steps[:turn]
    assert mode.is_euclidean == cycle.is_euclidean


@given(st.integers(1, 24), st.data())
def test_euclidean_cycles_are_maximally_even(size, data):
    count = data.draw(st.integers(0, size))
    cycle = Cycle.euclidean(size, count)
    assert len(cycle.onsets) == count
    assert cycle.is_euclidean
    assert len(set(cycle.steps)) <= 2
    assert max(cycle.steps, default=0) - min(cycle.steps, default=0) <= 1
    if count and math.gcd(size, count) == 1:
        generator = pow(count, -1, size)
        assert any(Cycle.generated(size, generator, count).rotate(pulses) == cycle for pulses in range(size))


def test_cycles_share_their_structure_with_scales():
    assert Cycle.euclidean(8, 3).steps == (2, 3, 3)
    assert Cycle.generated(8, 3, 3).steps == (3, 3, 2)
    assert Cycle.generated(12, 7, 7).mode(4).steps == (2, 2, 1, 2, 2, 2, 1)
    assert Cycle.generated(12, 7, 5).steps == (2, 2, 3, 2, 3)
    assert not Cycle(8, (0, 1, 2)).is_euclidean
    assert Cycle.euclidean(3, 3) | Cycle.euclidean(4, 4) == Cycle(12, (0, 3, 4, 6, 8, 9))
    assert Cycle.euclidean(3, 3) & Cycle.euclidean(4, 4) == Cycle(12, (0,))


def test_invalid_cycles():
    for size, onsets in ((0, ()), (-1, ()), (4, (4,)), (4, (-1,))):
        with pytest.raises(ValueError, match=r"pulse"):
            Cycle(size, onsets)
    for size, onsets in ((4.0, ()), (True, ()), (4, (1.0,)), (4, (True,))):
        with pytest.raises(TypeError, match="integer"):
            Cycle(size, onsets)  # ty: ignore[invalid-argument-type]
    with pytest.raises(RhythmError, match="returns to an onset"):
        Cycle.generated(8, 2, 5)
    for arguments in ((0, 3, 1), (8, 3, -1)):
        with pytest.raises(ValueError, match=r"pulse|negative"):
            Cycle.generated(*arguments)
    for arguments in ((4, 5), (4, -1), (0, 0)):
        with pytest.raises(ValueError, match=r"fit|pulse"):
            Cycle.euclidean(*arguments)
    cycle = Cycle(4, (0,))
    for operation in (lambda: cycle.refine(0), lambda: cycle.repeat(0)):
        with pytest.raises(ValueError, match="positive"):
            operation()
    with pytest.raises(TypeError):
        cycle | 4  # ty: ignore[unsupported-operator]


@given(st.fractions(0, 8, max_denominator=12), st.fractions(0, 8, max_denominator=12))
def test_tempo_is_linear_and_the_map_is_piecewise(first, second):
    tempo = Tempo(quarter, 120.0)
    assert tempo.seconds(quarter) == 0.5
    assert tempo.seconds(Duration(first) + Duration(second)) == pytest.approx(
        tempo.seconds(Duration(first)) + tempo.seconds(Duration(second))
    )
    changes = TempoMap(((Position(0), tempo), (Position(1), Tempo(quarter, 60.0))))
    low, high = sorted((Position(first), Position(second)))
    assert changes.seconds(low) <= changes.seconds(high)
    assert changes.seconds(Position(1)) == 2.0
    assert changes.seconds(Position(2)) == 6.0
    assert changes.seconds(Position(-1)) == -2.0
    assert TempoMap(((Position(0), tempo),)).seconds(low) == pytest.approx(tempo.seconds(low - Position(0)))


def test_invalid_tempos():
    for beat, rate in (
        (Duration(0), 120),
        (-quarter, 120),
        (quarter, 0),
        (quarter, -1),
        (quarter, math.inf),
        (quarter, math.nan),
    ):
        with pytest.raises(ValueError, match="positive"):
            Tempo(beat, rate)
    for beat, rate in ((Fraction(1, 4), 120), (quarter, True)):
        with pytest.raises(TypeError, match="Duration beat"):
            Tempo(beat, rate)  # ty: ignore[invalid-argument-type]
    tempo = Tempo(quarter, 120)
    for changes in ((), ((Position(1), tempo), (Position(0), tempo)), ((Position(0), tempo), (Position(0), tempo))):
        with pytest.raises(ValueError, match="strictly rising"):
            TempoMap(changes)
    for changes in (((Position(0),),), ((0, tempo),), ((Position(0), 120),)):
        with pytest.raises(TypeError, match="pairs"):
            TempoMap(changes)  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError, match="Position"):
        TempoMap(((Position(0), tempo),)).seconds(quarter)  # ty: ignore[invalid-argument-type]
    with pytest.raises(ValueError, match="range of a float"):
        tempo.seconds(Duration(10**400))


@given(parts(), parts(), parts(), factors, positions)
def test_duration_is_a_homomorphism_of_both_compositions(x, y, z, factor, start):
    assert (x + y).duration == x.duration + y.duration
    assert (x | y).duration == max(x.duration, y.duration)
    assert (x + y) + z == x + (y + z)
    assert (x | y) | z == x | (y | z)
    assert Serial().duration == Parallel().duration == Duration(0)
    assert (x + Serial()).events(start) == (Serial() + x).events(start) == x.events(start)
    assert (x | Parallel()).events(start) == x.events(start)
    assert x.stretch(factor).duration == x.duration * factor
    assert (x + y).stretch(factor) == x.stretch(factor) + y.stretch(factor)
    assert (x | y).stretch(factor) == x.stretch(factor) | y.stretch(factor)
    assert x.stretch(1) == x
    assert hash(x.stretch(1)) == hash(x)


@given(parts(), parts(), positions)
def test_events_follow_the_compositions(x, y, start):
    first, second = x.events(start), y.events(start)
    later = y.events(start + x.duration)
    assert sorted((x + y).events(start)) == sorted(first + later)
    assert sorted((x | y).events(start)) == sorted(first + second)
    for placed in first:
        assert start <= placed.start
        assert placed.start + placed.duration <= start + x.duration
    assert [placed.start for placed in first] == sorted(placed.start for placed in first)
    assert [placed.value for placed in x.map(lambda value: value + 1).events(start)] == [
        placed.value + 1 for placed in first
    ]
    assert x.map(lambda value: value).events(start) == first


def test_structures_carry_pitches_and_rests():
    melody = Event(quarter, Pitch("C4")) + Event(eighth) + Event(eighth, Pitch("E4"))
    bass = Event(quarter * 2, Pitch("C3"))
    fifth = Pitch.notation.interval(Fraction(3, 2))
    events = (melody | bass).map(lambda pitch: pitch + fifth).events()
    assert events == (
        Placed(Position(0), quarter, Pitch("G4")),
        Placed(Position(0), quarter * 2, Pitch("G3")),
        Placed(Position(Fraction(3, 8)), eighth, Pitch("B4")),
    )
    assert (melody | bass).duration == quarter * 2


def test_invalid_structures():
    with pytest.raises(TypeError, match="Duration"):
        Event(Fraction(1, 4))  # ty: ignore[invalid-argument-type]
    with pytest.raises(ValueError, match="negative"):
        Event(-quarter)
    for cls in (Serial, Parallel):
        with pytest.raises(TypeError, match="Part objects"):
            cls((quarter,))  # ty: ignore[invalid-argument-type]
    event = Event(quarter, 1)
    for factor in (0, -1):
        with pytest.raises(ValueError, match="positive"):
            event.stretch(factor)
    with pytest.raises(TypeError, match="integer or a Fraction"):
        event.stretch(0.5)  # ty: ignore[invalid-argument-type]
    with pytest.raises(TypeError):
        event + quarter  # ty: ignore[unsupported-operator]
    with pytest.raises(TypeError):
        event | 1  # ty: ignore[unsupported-operator]


@given(st.integers(-4, 2), st.integers(0, 3), st.sampled_from([1, 3, 5, 7, 9]))
def test_note_values_decompose_durations(exponent, dots, division):
    note = NoteValue(Duration(Fraction(2) ** exponent), dots, division)
    found = NoteValue.of(note.duration)
    if math.gcd(2 ** (dots + 1) - 1, division) == 1:
        assert found == note
    assert found is None or found.duration == note.duration
    assert note.duration.primes <= {2, *Duration(Fraction(1, division)).primes}


def test_note_values_name_dots_and_tuplets():
    def parts_of(value):
        note = NoteValue.of(Duration(Fraction(value)))
        return None if note is None else (note.base.value, note.dots, note.division)

    assert parts_of("1/4") == (Fraction(1, 4), 0, 1)
    assert parts_of("3/8") == (Fraction(1, 4), 1, 1)
    assert parts_of("7/16") == (Fraction(1, 4), 2, 1)
    assert parts_of("1/12") == (Fraction(1, 8), 0, 3)
    assert parts_of("1/20") == (Fraction(1, 16), 0, 5)
    assert parts_of("3/20") == (Fraction(1, 8), 1, 5)
    assert parts_of("6") == (4, 1, 1)
    assert parts_of("5/16") is None
    assert parts_of("5/8") is None


def test_invalid_note_values():
    for value in (0, Fraction(-1, 4)):
        with pytest.raises(ValueError, match="positive"):
            NoteValue.of(Duration(value))
    with pytest.raises(TypeError, match="Duration"):
        NoteValue.of(Fraction(1, 4))  # ty: ignore[invalid-argument-type]
    for base in (Duration(Fraction(3, 8)), Duration(0), Duration(Fraction(1, 12)), Duration(-1)):
        with pytest.raises(ValueError, match="power of two"):
            NoteValue(base)
    for dots, division in ((-1, 1), (0, 0), (0, 2), (0, -3)):
        with pytest.raises(ValueError, match="odd division"):
            NoteValue(quarter, dots, division)
    for arguments in ((Fraction(1, 4),), (quarter, 1.0), (quarter, 0, True)):
        with pytest.raises(TypeError, match="Duration base"):
            NoteValue(*arguments)  # ty: ignore[invalid-argument-type]
