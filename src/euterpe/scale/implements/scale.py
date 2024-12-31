from ..diatonic import DiatonicScale, NondiatonicScale


class Major(
    DiatonicScale,
    intervals=(2, 2, 1, 2, 2, 2, 1),
):
    """Major Scale"""


class Minor(
    DiatonicScale,
    intervals=(2, 1, 2, 2, 1, 2, 2),
):
    """Minor Scale"""


class HarmonicMinor(
    DiatonicScale,
    intervals=(2, 1, 2, 2, 1, 3, 1),
):
    """Harmonic Minor Scale"""


class MelodicMinor(
    DiatonicScale,
    intervals=(2, 1, 2, 2, 2, 2, 1),
):
    """Melodic Minor Scale"""


class Pentatonic(
    NondiatonicScale,
    extensions=[[0], [0], [0], [], [0], [0], []],
    base=Major,
):
    """Pentatonic Scale"""


class MinorPentatonic(
    NondiatonicScale,
    extensions=[[0], [], [0], [0], [0], [], [0]],
    base=Minor,
):
    """MinorPentatonic Scale"""


class Bluenote(
    NondiatonicScale,
    extensions=[],
    base=HarmonicMinor,
):
    """Bluenote Scale"""


class Diminish(
    NondiatonicScale,
    extensions=[],
    base=Major,
):
    """Diminish Scale"""


class CombDiminish(
    NondiatonicScale,
    extensions=[],
    base=Major,
):
    """CombDiminish Scale"""


class Wholetone(
    NondiatonicScale,
    extensions=[],
    base=Major,
):
    """Wholetone Scale"""
