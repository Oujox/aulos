import pytest

from aulos.TET12 import (
    Bluenote,
    Equal12Tuner,
    HarmonicMinor,
    Ionian,
    Ionian_s5,
    JustIntonationTuner,
    Locrian,
    Lydian_f7,
    Major,
    Minor,
    Note,
    Pentatonic,
    PythagoreanTuner,
)


def test_Note_init_from_notename(data_notenames):
    for pitchname in data_notenames:
        assert isinstance(Note(pitchname), Note)


def test_Note_init_from_notenumber(data_notenumbers):
    for pitchclass in data_notenumbers:
        assert isinstance(Note(pitchclass), Note)


def test_Note_init_from_note_object(data_notenumbers):
    for notenumber in data_notenumbers:
        assert isinstance(Note(Note(notenumber)), Note)


@pytest.mark.parametrize(
    "invalid_value",
    ["", " ", "Cb-1", "G#9", -1, 128, None, [], {}],
)
def test_Note_init_from_invalid_value(invalid_value):
    with pytest.raises(ValueError):
        _ = Note(invalid_value)


def test_Note_property_get_notenumber(data_notenumbers, data_map_notename_to_notenumber):
    for notenumber in data_notenumbers:
        assert Note(notenumber).notenumber == notenumber
    for notename, notenumber in data_map_notename_to_notenumber.items():
        assert Note(notename).notenumber == notenumber


def test_Note_property_get_notename(data_notenumbers, data_notenames):
    for notenumber in data_notenumbers:
        assert Note(notenumber).notename is None
    for notename in data_notenames:
        assert Note(notename).notename == notename


def test_Note_property_get_notenames(
    data_notenumbers,
    data_notenames,
    data_map_notenumber_to_notenames,
    data_map_notename_to_notenumber,
):
    for notenumber in data_notenumbers:
        assert Note(notenumber).notenames == [
            item for item in data_map_notenumber_to_notenames[notenumber] if item is not None
        ]
    for notename in data_notenames:
        assert Note(notename).notenames == [
            item
            for item in data_map_notenumber_to_notenames[data_map_notename_to_notenumber[notename]]
            if item is not None
        ]


def test_Note_dunder_eqne(data_map_notename_to_notenumber):
    for notename, notenumber in data_map_notename_to_notenumber.items():
        assert not Note(notename) != notenumber
        assert not Note(notenumber) != notenumber
        assert not Note(notename) != Note(notenumber)
        assert not Note(notenumber) != Note(notename)


def test_PitchClass_dunder_eqne_notimplemented(data_notenumbers):
    for notenumber in data_notenumbers:
        assert not Note(notenumber) == object()


def test_Note_dunder_add(data_notenumbers):
    for notenumber1 in data_notenumbers:
        for notenumber2 in data_notenumbers:
            if (notenumber1 + notenumber2) in data_notenumbers:
                assert (Note(notenumber1) + notenumber2) == (notenumber1 + notenumber2)
            else:
                with pytest.raises(ValueError):
                    _ = Note(notenumber1) + notenumber2


def test_Note_dunder_sub(data_notenumbers):
    for notenumber1 in data_notenumbers:
        for notenumber2 in data_notenumbers:
            if (notenumber1 - notenumber2) in data_notenumbers:
                assert (Note(notenumber1) - notenumber2) == (notenumber1 - notenumber2)
            else:
                with pytest.raises(ValueError):
                    _ = Note(notenumber1) - notenumber2


def test_Note_dunder_int(data_notenumbers):
    for notenumber in data_notenumbers:
        assert int(Note(notenumber)) == notenumber


def test_Note_dunder_str(
    data_notenumbers,
    data_notenames,
    data_map_notenumber_to_notenames,
):
    for notenumber in data_notenumbers:
        notenames = [name for name in data_map_notenumber_to_notenames[notenumber] if name is not None]
        assert str(Note(notenumber)) == f"<Note: {notenames}, scale: None>"
    for notename in data_notenames:
        assert str(Note(notename)) == f"<Note: {notename}, scale: None>"


def test_Note_dunder_repr(
    data_notenumbers,
    data_notenames,
    data_map_notenumber_to_notenames,
):
    for notenumber in data_notenumbers:
        notenames = [name for name in data_map_notenumber_to_notenames[notenumber] if name is not None]
        assert repr(Note(notenumber)) == f"<Note: {notenames}, scale: None>"
    for notename in data_notenames:
        assert repr(Note(notename)) == f"<Note: {notename}, scale: None>"


@pytest.mark.parametrize(
    ("scale", "key", "notenumber", "expected"),
    [
        (Major, "C", 64, "E4"),
        (Minor, "C", 64, None),
        (HarmonicMinor, "C", 64, None),
        (Pentatonic, "C", 64, "E4"),
        (Bluenote, "C", 64, "E4"),
        (Ionian, "C", 64, "E4"),
        (Ionian_s5, "C", 64, "E4"),
        (Locrian, "C", 64, None),
        (Lydian_f7, "C", 64, "E4"),
    ],
)
def test_Note_init_with_scale(scale, key, notenumber, expected):
    pc = Note(notenumber, scale=scale(key))
    assert isinstance(pc, Note)
    assert pc.notename == expected


@pytest.mark.parametrize(
    ("tuner", "root", "notenumber", "expected"),
    [
        (JustIntonationTuner, 440, 67, 660.0),
        (PythagoreanTuner, 440, 67, 660.0),
        (Equal12Tuner, 440, 67, 659.2551138257401),
    ],
)
def test_Note_init_with_tuner(tuner, root, notenumber, expected):
    pc = Note(notenumber, tuner=tuner(root))
    assert isinstance(pc, Note)
    assert pc.hz == expected
