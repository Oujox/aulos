import typing as t


def compress_ratio(ratio: float) -> float:
    while ratio > 2:
        ratio = ratio / 2
    while ratio < 1:
        ratio = ratio * 2
    return ratio


def standard_tuning_table(p5th_ratio: float) -> tuple[float]:
    # https://en.wikipedia.org/wiki/Just_intonation#Five-limit_tuning
    (ratios := [compress_ratio(p5th_ratio**i) for i in range(12)]).sort()

    return tuple(ratios)


def fivelimit_tuning_table() -> tuple[float]:
    # https://en.wikipedia.org/wiki/Just_intonation#Five-limit_tuning
    (
        ratios := [
            compress_ratio((3**j) * (5**i))
            for i in range(-1, 1 + 1)
            for j in range(-2, 2 + 1)
            if not j == -2
        ]
    ).sort()

    return tuple(ratios)


PYTHAGOREAN_TUNING_RATIOS: t.Final[tuple[float]] = standard_tuning_table(1.5)
MEANTONE_TUNING_RATIOS: t.Final[tuple[float]] = standard_tuning_table(5**0.25)
FIVELIMIT_TUNING_RATIOS: t.Final[tuple[float]] = fivelimit_tuning_table()
