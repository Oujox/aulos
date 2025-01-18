import pytest

from src.euterpe.note import _PitchClass
from src.euterpe.scale import Locrian, Major, Minor


def test_PitchClass_init_from_pitchname(setting, data_pitchname):
    for pitchname in data_pitchname:
        assert isinstance(_PitchClass(pitchname, setting=setting), _PitchClass)


def test_PitchClass_init_from_pitchclass(setting, data_pitchclass):
    for pitchclass in data_pitchclass:
        assert isinstance(_PitchClass(pitchclass, setting=setting), _PitchClass)


@pytest.mark.parametrize(
    "invalid_value",
    [
        "",
        " ",
        -1,
        None,
        [],
        {},
    ],
)
def test_PitchClass_init_from_invalid_value(setting, invalid_value):
    with pytest.raises(ValueError):
        _ = _PitchClass(invalid_value, setting=setting)


def test_PitchClass_property_get_pitchclass(setting, data_pitchclass):
    for pitchclass in data_pitchclass:
        assert _PitchClass(pitchclass, setting=setting).pitchclass == pitchclass


def test_PitchClass_property_get_pitchname(setting, data_pitchclass, data_pitchname):
    for pitchclass in data_pitchclass:
        assert _PitchClass(pitchclass, setting=setting).pitchname == None
    for pitchname in data_pitchname:
        assert _PitchClass(pitchname, setting=setting).pitchname == pitchname


def test_PitchClass_property_get_pitchnames(
    setting,
    data_pitchclass,
    data_pitchname,
    data_map_pitchclass_to_pitchnames,
    data_map_pitchname_to_pitchclass,
):
    for pitchclass in data_pitchclass:
        assert _PitchClass(pitchclass, setting=setting).pitchnames == [
            item
            for item in data_map_pitchclass_to_pitchnames[pitchclass]
            if item is not None
        ]
    for pitchname in data_pitchname:
        assert _PitchClass(pitchname, setting=setting).pitchnames == [
            item
            for item in data_map_pitchclass_to_pitchnames[
                data_map_pitchname_to_pitchclass[pitchname]
            ]
            if item is not None
        ]


def test_PitchClass_dunder_eqne(setting, data_map_pitchname_to_pitchclass):
    for pitchname, pitchclass in data_map_pitchname_to_pitchclass.items():
        assert not _PitchClass(pitchname, setting=setting) != pitchclass
        assert not _PitchClass(pitchclass, setting=setting) != pitchclass
        assert not _PitchClass(pitchname, setting=setting) != _PitchClass(
            pitchclass, setting=setting
        )
        assert not _PitchClass(pitchclass, setting=setting) != _PitchClass(
            pitchname, setting=setting
        )


def test_PitchClass_dunder_add(setting, data_pitchclass):
    for pitchclass in data_pitchclass:
        for pitchclass2 in data_pitchclass:
            assert (_PitchClass(pitchclass, setting=setting) + pitchclass2) == (
                pitchclass + pitchclass2
            ) % sum(setting.pitchclass.intervals)


def test_PitchClass_dunder_sub(setting, data_pitchclass):
    for pitchclass in data_pitchclass:
        for pitchclass2 in data_pitchclass:
            assert (_PitchClass(pitchclass, setting=setting) - pitchclass2) == (
                pitchclass - pitchclass2
            ) % sum(setting.pitchclass.intervals)


def test_PitchClass_dunder_int(setting, data_pitchclass):
    for pitchclass in data_pitchclass:
        assert int(_PitchClass(pitchclass, setting=setting)) == pitchclass


def test_PitchClass_dunder_str(
    setting, data_pitchclass, data_pitchname, data_map_pitchclass_to_pitchnames
):
    for pitchclass in data_pitchclass:
        pitchnames = [
            name
            for name in data_map_pitchclass_to_pitchnames[pitchclass]
            if name is not None
        ]
        assert (
            str(_PitchClass(pitchclass, setting=setting))
            == f"<PitchClass: {pitchnames}, scale: None>"
        )
    for pitchname in data_pitchname:
        assert (
            str(_PitchClass(pitchname, setting=setting))
            == f"<PitchClass: {pitchname}, scale: None>"
        )
