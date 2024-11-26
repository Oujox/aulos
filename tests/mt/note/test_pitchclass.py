import pytest
from src.mt.note import PitchClass
from src.mt.scale import Major, Minor, Locrian


def test_PitchClass_init_from_pitchname(setting, data_pitchname):
    for pitchname in data_pitchname:
        assert isinstance(PitchClass(pitchname, setting=setting), PitchClass)


def test_PitchClass_init_from_pitchclass(setting, data_pitchclass):
    for pitchclass in data_pitchclass:
        assert isinstance(PitchClass(pitchclass, setting=setting), PitchClass)


@pytest.mark.parametrize(
    "invalid_value",
    [
        "",
        " ",
        "0",
        "a",
        "bb",
        "c##",
        "A@",
        "A@#",
        "A#@#",
        "H",
        "H#",
        "Hbb",
        "A1",
        "Ab1",
        "A###",
        "Abbb",
        "#A",
        "bbA",
        -1,
        12,
        None,
        [],
        {},
    ],
)
def test_PitchClass_init_from_invalid_value(setting, invalid_value):
    with pytest.raises(ValueError):
        _ = PitchClass(invalid_value, setting=setting)


def test_PitchClass_property_get_pitchclass(setting, data_pitchclass):
    for pitchclass in data_pitchclass:
        assert PitchClass(pitchclass, setting=setting).pitchclass == pitchclass


def test_PitchClass_property_get_pitchname(setting, data_pitchclass, data_pitchname):
    for pitchclass in data_pitchclass:
        assert PitchClass(pitchclass, setting=setting).pitchname == None
    for pitchname in data_pitchname:
        assert PitchClass(pitchname, setting=setting).pitchname == pitchname


def test_PitchClass_property_get_pitchnames(
    setting,
    data_pitchclass,
    data_pitchname,
    data_map_pitchclass_to_pitchnames,
    data_map_pitchname_to_pitchclass,
):
    for pitchclass in data_pitchclass:
        assert PitchClass(pitchclass, setting=setting).pitchnames == [
            item
            for item in data_map_pitchclass_to_pitchnames[pitchclass]
            if item is not None
        ]
    for pitchname in data_pitchname:
        assert PitchClass(pitchname, setting=setting).pitchnames == [
            item
            for item in data_map_pitchclass_to_pitchnames[
                data_map_pitchname_to_pitchclass[pitchname]
            ]
            if item is not None
        ]


def test_PitchClass_dunder_eqne(setting, data_map_pitchname_to_pitchclass):
    for pitchname, pitchclass in data_map_pitchname_to_pitchclass.items():
        assert not PitchClass(pitchname, setting=setting) != pitchclass
        assert not PitchClass(pitchclass, setting=setting) != pitchclass
        assert not PitchClass(pitchname, setting=setting) != PitchClass(
            pitchclass, setting=setting
        )
        assert not PitchClass(pitchclass, setting=setting) != PitchClass(
            pitchname, setting=setting
        )


def test_PitchClass_dunder_add(setting):
    assert 1


def test_PitchClass_dunder_sub(setting):
    assert 1


def test_PitchClass_dunder_int(setting, data_pitchclass):
    for pitchclass in data_pitchclass:
        assert int(PitchClass(pitchclass, setting=setting)) == pitchclass


def test_PitchClass_dunder_str(setting, data_pitchclass, data_pitchname):
    for pitchclass in data_pitchclass:
        assert str(PitchClass(pitchclass, setting=setting)) == ""
    for pitchname in data_pitchname:
        assert str(PitchClass(pitchname, setting=setting)) == pitchname
