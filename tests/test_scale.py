import pytest

from aulos.TET12 import (
    Bluenote,
    HarmonicMinor,
    Ionian,
    Ionian_s5,
    Key,
    Locrian,
    Lydian_f7,
    Major,
    Minor,
    Pentatonic,
)


@pytest.mark.parametrize(
    "scale",
    [
        Major,
        Minor,
        HarmonicMinor,
        Pentatonic,
        Bluenote,
        Ionian,
        Ionian_s5,
        Locrian,
        Lydian_f7,
    ],
)
def test_Scale_init_str(scale, data_keynames):
    for keyname in data_keynames:
        assert isinstance(scale(keyname), scale)


@pytest.mark.parametrize(
    "scale",
    [
        Major,
        Minor,
        HarmonicMinor,
        Pentatonic,
        Bluenote,
        Ionian,
        Ionian_s5,
        Locrian,
        Lydian_f7,
    ],
)
def test_Scale_init_key(scale, data_keynames):
    for keyname in data_keynames:
        assert isinstance(scale(Key(keyname)), scale)


@pytest.mark.parametrize(
    ("scale", "keyname", "expected_components"),
    [
        (Major, "C", ["C", "D", "E", "F", "G", "A", "B"]),
        (Minor, "C", ["C", "D", "Eb", "F", "G", "Ab", "Bb"]),
        (HarmonicMinor, "C", ["C", "D", "Eb", "F", "G", "Ab", "B"]),
        (Pentatonic, "C", ["C", "D", "E", "G", "A"]),
        (Bluenote, "C", ["C", "D", "Eb", "E", "F", "Gb", "G", "A", "Bb", "B"]),
        (Ionian, "C", ["C", "D", "E", "F", "G", "A", "B"]),
        (Ionian_s5, "C", ["C", "D", "E", "F", "G#", "A", "B"]),
        (Locrian, "C", ["C", "Db", "Eb", "F", "Gb", "Ab", "Bb"]),
        (Lydian_f7, "C", ["C", "D", "E", "F#", "G", "A", "Bb"]),
    ],
)
def test_Scale_components(scale, keyname, expected_components):
    scale_instance = scale(keyname)
    components = [pitchclass.pitchname for pitchclass in scale_instance.components]
    assert components == expected_components
