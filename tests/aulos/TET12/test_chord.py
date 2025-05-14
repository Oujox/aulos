import pytest

from aulos.TET12 import Chord


@pytest.mark.parametrize(
    ("chord", "octave"),
    [
        ("C", 5),
        ("Cm", 5),
        ("Cm7", 5),
        ("Cm7/Bb", 5),
        ("Cm7/B", 5),
    ],
)
def test_Chord_init(chord, octave):
    assert isinstance(Chord((chord, octave)), Chord)
