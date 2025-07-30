import pytest

from aulos.TET12 import (
    Equal12Tuner,
    JustIntonationTuner,
    PythagoreanTuner,
)


@pytest.mark.parametrize(
    "tuner",
    [
        Equal12Tuner,
        JustIntonationTuner,
        PythagoreanTuner,
    ],
)
def test_Tuner_init(tuner):
    assert isinstance(tuner(440), tuner)
