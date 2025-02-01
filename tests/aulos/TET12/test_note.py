import pytest

from src.aulos.TET12 import Note


def test_Note_init_from_notename(data_notenames):
    for pitchname in data_notenames:
        assert isinstance(Note(pitchname), Note)


def test_Note_init_from_notenumber(data_notenumbers):
    for pitchclass in data_notenumbers:
        assert isinstance(Note(pitchclass), Note)


@pytest.mark.parametrize(
    "invalid_value",
    ["", " ", "Cb-1", "G#9", -1, 128, None, [], {}],
)
def test_Note_init_from_invalid_value(invalid_value):
    with pytest.raises(ValueError):
        _ = Note(invalid_value)


def test_Note_property_get_notenumber(data_notenumbers):
    for notenumber in data_notenumbers:
        assert Note(notenumber).notenumber == notenumber


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


def test_PitchClass_dunder_str(
    data_notenumbers,
    data_notenames,
    data_map_notenumber_to_notenames,
):
    for notenumber in data_notenumbers:
        notenames = [name for name in data_map_notenumber_to_notenames[notenumber] if name is not None]
        assert str(Note(notenumber)) == f"<Note: {notenames}, scale: None>"
    for notename in data_notenames:
        assert str(Note(notename)) == f"<Note: {notename}, scale: None>"
