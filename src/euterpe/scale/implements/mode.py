from ..implements.scale import HarmonicMinor, Major, MelodicMinor
from ..mode import Mode


class Ionian(
    Mode,
    Major,
    shift=0,
    intervals=Major.intervals,
): ...


class Dorian(
    Mode,
    Major,
    shift=1,
    intervals=Major.intervals,
): ...


class Phrygian(
    Mode,
    Major,
    shift=2,
    intervals=Major.intervals,
): ...


class Lydian(
    Mode,
    Major,
    shift=3,
    intervals=Major.intervals,
): ...


class Mixolydian(
    Mode,
    Major,
    shift=4,
    intervals=Major.intervals,
): ...


class Aeorian(
    Mode,
    Major,
    shift=5,
    intervals=Major.intervals,
): ...


class Locrian(
    Mode,
    Major,
    shift=6,
    intervals=Major.intervals,
): ...


class Dorian_f2(
    Mode,
    MelodicMinor,
    shift=1,
    intervals=MelodicMinor.intervals,
): ...


class Lydian_s5(
    Mode,
    MelodicMinor,
    shift=2,
    intervals=MelodicMinor.intervals,
): ...


class Lydian_f7(
    Mode,
    MelodicMinor,
    shift=3,
    intervals=MelodicMinor.intervals,
): ...


class Mixolydian_f6(
    Mode,
    MelodicMinor,
    shift=4,
    intervals=MelodicMinor.intervals,
): ...


class Aeorian_f5(
    Mode,
    MelodicMinor,
    shift=5,
    intervals=MelodicMinor.intervals,
): ...


class SuperLocrian(
    Mode,
    MelodicMinor,
    shift=6,
    intervals=MelodicMinor.intervals,
): ...


class Locrian_n6(
    Mode,
    HarmonicMinor,
    shift=1,
    intervals=HarmonicMinor.intervals,
): ...


class Ionian_s5(
    Mode,
    HarmonicMinor,
    shift=2,
    intervals=HarmonicMinor.intervals,
): ...


class Dorian_s4(
    Mode,
    HarmonicMinor,
    shift=3,
    intervals=HarmonicMinor.intervals,
): ...


class Mixolydian_f9(
    Mode,
    HarmonicMinor,
    shift=4,
    intervals=HarmonicMinor.intervals,
): ...  # PhrygianDominant


class Lydian_s2(
    Mode,
    HarmonicMinor,
    shift=5,
    intervals=HarmonicMinor.intervals,
): ...


class AlteredSuperLocrian(
    Mode,
    HarmonicMinor,
    shift=6,
    intervals=HarmonicMinor.intervals,
): ...
