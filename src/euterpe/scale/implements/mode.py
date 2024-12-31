from ..implements.scale import HarmonicMinor, Major, MelodicMinor
from ..mode import Mode


class Ionian(
    Mode,
    Major,
    intervals=Major.intervals,
    shift=0,
): ...


class Dorian(
    Mode,
    Major,
    intervals=Major.intervals,
    shift=1,
): ...


class Phrygian(
    Mode,
    Major,
    intervals=Major.intervals,
    shift=2,
): ...


class Lydian(
    Mode,
    Major,
    intervals=Major.intervals,
    shift=3,
): ...


class Mixolydian(
    Mode,
    Major,
    intervals=Major.intervals,
    shift=4,
): ...


class Aeorian(
    Mode,
    Major,
    intervals=Major.intervals,
    shift=5,
): ...


class Locrian(
    Mode,
    Major,
    intervals=Major.intervals,
    shift=6,
): ...


class Dorian_f2(
    Mode,
    MelodicMinor,
    intervals=MelodicMinor.intervals,
    shift=1,
): ...


class Lydian_s5(
    Mode,
    MelodicMinor,
    intervals=MelodicMinor.intervals,
    shift=2,
): ...


class Lydian_f7(
    Mode,
    MelodicMinor,
    intervals=MelodicMinor.intervals,
    shift=3,
): ...


class Mixolydian_f6(
    Mode,
    MelodicMinor,
    intervals=MelodicMinor.intervals,
    shift=4,
): ...


class Aeorian_f5(
    Mode,
    MelodicMinor,
    intervals=MelodicMinor.intervals,
    shift=5,
): ...


class SuperLocrian(
    Mode,
    MelodicMinor,
    intervals=MelodicMinor.intervals,
    shift=6,
): ...


class Locrian_n6(
    Mode,
    HarmonicMinor,
    intervals=HarmonicMinor.intervals,
    shift=1,
): ...


class Ionian_s5(
    Mode,
    HarmonicMinor,
    intervals=HarmonicMinor.intervals,
    shift=2,
): ...


class Dorian_s4(
    Mode,
    HarmonicMinor,
    intervals=HarmonicMinor.intervals,
    shift=3,
): ...


class Mixolydian_f9(
    Mode,
    HarmonicMinor,
    intervals=HarmonicMinor.intervals,
    shift=4,
): ...  # PhrygianDominant


class Lydian_s2(
    Mode,
    HarmonicMinor,
    intervals=HarmonicMinor.intervals,
    shift=5,
): ...


class AlteredSuperLocrian(
    Mode,
    HarmonicMinor,
    intervals=HarmonicMinor.intervals,
    shift=6,
): ...
