from ..scale import Scale


class Major(Scale, intervals=(2, 2, 1, 2, 2, 2, 1)):
    """Major Scale"""


class Minor(Scale, intervals=(2, 1, 2, 2, 1, 2, 2)):
    """Minor Scale"""


class HarmonicMinor(Scale, intervals=(2, 1, 2, 2, 1, 3, 1)):
    """Harmonic Minor Scale"""


class MelodicMinor(Scale, intervals=(2, 1, 2, 2, 2, 2, 1)):
    """Melodic Minor Scale"""


class HarmonicMinorP5thBelow(Scale, intervals=(1, 3, 1, 2, 1, 2, 2)):
    """Harmonic Minor P5th Below Scale"""


class Pentatonic(Scale, intervals=(2, 2, 0, 3, 2, 0, 3)):
    """Pentatonic Scale"""


class MinorPentatonic(Scale, intervals=(3, 2, 2, 0, 3, 2, 0)):
    """MinorPentatonic Scale"""


class Bluenote(Scale, intervals=(2, 1, 1, 1, 1, 1, 2, 1, 1, 1)):
    """Bluenote Scale"""


class Diminish(Scale, intervals=(2, 1, 2, 1, 2, 1, 2, 1)):
    """Diminish Scale"""


class CombDiminish(Scale, intervals=(1, 2, 1, 2, 1, 2, 1, 2)):
    """CombDiminish Scale"""


class Wholetone(Scale, intervals=(2, 2, 2, 2, 2, 0, 2)):
    """Wholetone Scale"""
