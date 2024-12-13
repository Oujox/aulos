from ..implements.scale import HarmonicMinor, Major, MelodicMinor
from ..mode import Mode


class Ionian(
    Mode,
    scale=Major,
    intervals=(2, 2, 1, 2, 2, 2, 1),
): ...


class Dorian(
    Mode,
    scale=Major,
    intervals=(2, 1, 2, 2, 2, 1, 2),
): ...


class Phrygian(
    Mode,
    scale=Major,
    intervals=(1, 2, 2, 2, 1, 2, 2),
): ...


class Lydian(
    Mode,
    scale=Major,
    intervals=(2, 2, 2, 1, 2, 2, 1),
): ...


class Mixolydian(
    Mode,
    scale=Major,
    intervals=(2, 2, 1, 2, 2, 1, 2),
): ...


class Aeorian(
    Mode,
    scale=Major,
    intervals=(2, 1, 2, 2, 1, 2, 2),
): ...


class Locrian(
    Mode,
    scale=Major,
    intervals=(1, 2, 2, 1, 2, 2, 2),
): ...


class Dorian_f2(
    Mode,
    scale=MelodicMinor,
    intervals=(1, 2, 2, 2, 2, 1, 2),
): ...


class Lydian_s5(
    Mode,
    scale=MelodicMinor,
    intervals=(2, 2, 2, 2, 1, 2, 1),
): ...


class Lydian_f7(
    Mode,
    scale=MelodicMinor,
    intervals=(2, 2, 2, 1, 2, 1, 2),
): ...


class Mixolydian_f6(
    Mode,
    scale=MelodicMinor,
    intervals=(2, 2, 1, 2, 1, 2, 2),
): ...


class Aeorian_f5(
    Mode,
    scale=MelodicMinor,
    intervals=(2, 1, 2, 1, 2, 2, 2),
): ...


class SuperLocrian(
    Mode,
    scale=MelodicMinor,
    intervals=(1, 2, 1, 2, 2, 2, 2),
): ...


class Locrian_n6(
    Mode,
    scale=HarmonicMinor,
    intervals=(1, 2, 2, 1, 3, 1, 2),
): ...


class Ionian_s5(
    Mode,
    scale=HarmonicMinor,
    intervals=(2, 2, 1, 3, 1, 2, 1),
): ...


class Dorian_s4(
    Mode,
    scale=HarmonicMinor,
    intervals=(2, 1, 3, 1, 2, 1, 2),
): ...


class Mixolydian_f9(
    Mode,
    scale=HarmonicMinor,
    intervals=(1, 3, 1, 2, 1, 2, 2),
): ...  # PhrygianDominant


class Lydian_s2(
    Mode,
    scale=HarmonicMinor,
    intervals=(3, 1, 2, 1, 2, 2, 1),
): ...


class AlteredSuperLocrian(
    Mode,
    scale=HarmonicMinor,
    intervals=(1, 2, 1, 2, 2, 1, 3),
): ...
