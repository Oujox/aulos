from ..tuner import Tuner
from .ratios import (FIVELIMIT_TUNING_RATIOS, MEANTONE_TUNING_RATIOS,
                     PYTHAGOREAN_TUNING_RATIOS, standard_tuning_table)


class JustIntonationTuner(
    Tuner,
    ratios=FIVELIMIT_TUNING_RATIOS,
): ...


class MeantoneTuner(
    Tuner,
    ratios=MEANTONE_TUNING_RATIOS,
): ...


class PythagoreanTuner(
    Tuner,
    ratios=PYTHAGOREAN_TUNING_RATIOS,
): ...


class Equal12Tuner(
    Tuner,
    ratios=standard_tuning_table(2 ** (1 / 12)),
): ...
