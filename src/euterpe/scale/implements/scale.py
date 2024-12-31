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
    extensions=[[0], [0], [-1, 0], [0], [-1, 0], [0], [-1, 0]],
    base=Major,
):
    """Bluenote Scale"""


class Diminish(
    NondiatonicScale,
    extensions=[[0], [0], [-1], [0, 1], [1], [0], [0]],
    base=Major,
):
    """Diminish Scale"""


class CombDiminish(
    NondiatonicScale,
    extensions=[[0], [-1], [-1, 0], [1], [0], [0], [-1]],
    base=Major,
):
    """CombDiminish Scale"""


class Wholetone(
    NondiatonicScale,
    extensions=[[0], [0], [0], [1], [1], [1], []],
    base=Major,
):
    """Wholetone Scale"""
