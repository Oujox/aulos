import typing as t

from ..quality import Quality

# Triadic chords


class major(
    Quality,
    name="",
    areas=("maj",),
    positions=(0, 4, 7),
): ...


class minor(
    Quality,
    name="m",
    areas=("min",),
    positions=(0, 3, 7),
): ...


class augmented(
    Quality,
    name="arg",
    areas=(),
    positions=(0, 4, 8),
): ...


class diminished(
    Quality,
    name="dim",
    areas=(),
    positions=(0, 3, 6),
): ...


class suspended2(
    Quality,
    name="sus2",
    areas=(),
    positions=(0, 2, 7),
): ...


class suspended4(
    Quality,
    name="sus4",
    areas=(),
    positions=(0, 5, 7),
): ...


# Tertian chords


class dominant6(
    Quality,
    name="6",
    areas=(),
    positions=(0, 4, 7, 9),
): ...


class dominant7(
    Quality,
    name="7",
    areas=(),
    positions=(0, 4, 7, 10),
): ...


class dominantMajor7(
    Quality,
    name="M7",
    areas=(),
    positions=(0, 4, 7, 11),
): ...


class minor6(
    Quality,
    name="m6",
    areas=(),
    positions=(0, 3, 7, 9),
): ...


class minor7(
    Quality,
    name="m7",
    areas=(),
    positions=(0, 3, 7, 10),
): ...


class minorMajor7(
    Quality,
    name="mM7",
    areas=(),
    positions=(0, 3, 7, 11),
): ...


class augmented6(
    Quality,
    name="aug6",
    areas=(),
    positions=(0, 4, 8, 9),
): ...


class augmented7(
    Quality,
    name="aug7",
    areas=(),
    positions=(0, 4, 8, 10),
): ...


class augmentedMajor7(
    Quality,
    name="augM7",
    areas=(),
    positions=(0, 4, 8, 11),
): ...


class diminished7(
    Quality,
    name="dim7",
    areas=(),
    positions=(0, 3, 6, 9),
): ...
