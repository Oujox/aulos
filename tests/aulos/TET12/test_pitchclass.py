import pytest

from src.aulos.TET12 import PitchClass


def test_PitchClass_init_from_pitchname(data_pitchname):
    for pitchname in data_pitchname:
        assert isinstance(PitchClass(pitchname), PitchClass)


def test_PitchClass_init_from_pitchclass(data_pitchclass):
    for pitchclass in data_pitchclass:
        assert isinstance(PitchClass(pitchclass), PitchClass)


@pytest.mark.parametrize(
    "invalid_value",
    ["", " ", "a", "g", "@", "H", -1, 12, None, [], {}],
)
def test_PitchClass_init_from_invalid_value(invalid_value):
    with pytest.raises(ValueError):
        _ = PitchClass(invalid_value)


def test_PitchClass_property_get_pitchclass(data_pitchclass):
    for pitchclass in data_pitchclass:
        assert PitchClass(pitchclass).pitchclass == pitchclass


def test_PitchClass_property_get_pitchname(data_pitchclass, data_pitchname):
    for pitchclass in data_pitchclass:
        assert PitchClass(pitchclass).pitchname is None
    for pitchname in data_pitchname:
        assert PitchClass(pitchname).pitchname == pitchname


def test_PitchClass_property_get_pitchnames(
    data_pitchclass,
    data_pitchname,
    data_map_pitchclass_to_pitchnames,
    data_map_pitchname_to_pitchclass,
):
    for pitchclass in data_pitchclass:
        assert PitchClass(pitchclass).pitchnames == [
            item
            for item in data_map_pitchclass_to_pitchnames[pitchclass]
            if item is not None
        ]
    for pitchname in data_pitchname:
        assert PitchClass(pitchname).pitchnames == [
            item
            for item in data_map_pitchclass_to_pitchnames[
                data_map_pitchname_to_pitchclass[pitchname]
            ]
            if item is not None
        ]


def test_PitchClass_dunder_eqne(data_map_pitchname_to_pitchclass):
    for pitchname, pitchclass in data_map_pitchname_to_pitchclass.items():
        assert not PitchClass(pitchname) != pitchclass
        assert not PitchClass(pitchclass) != pitchclass
        assert not PitchClass(pitchname) != PitchClass(pitchclass)
        assert not PitchClass(pitchclass) != PitchClass(pitchname)


def test_PitchClass_dunder_add(data_pitchclass):
    for pitchclass in data_pitchclass:
        for pitchclass2 in data_pitchclass:
            assert (PitchClass(pitchclass) + pitchclass2) == (
                pitchclass + pitchclass2
            ) % sum(PitchClass.schema.intervals)


def test_PitchClass_dunder_sub(data_pitchclass):
    for pitchclass in data_pitchclass:
        for pitchclass2 in data_pitchclass:
            assert (PitchClass(pitchclass) - pitchclass2) == (
                pitchclass - pitchclass2
            ) % sum(PitchClass.schema.intervals)


def test_PitchClass_dunder_int(data_pitchclass):
    for pitchclass in data_pitchclass:
        assert int(PitchClass(pitchclass)) == pitchclass


def test_PitchClass_dunder_str(
    data_pitchclass, data_pitchname, data_map_pitchclass_to_pitchnames,
):
    for pitchclass in data_pitchclass:
        pitchnames = [
            name
            for name in data_map_pitchclass_to_pitchnames[pitchclass]
            if name is not None
        ]
        assert str(PitchClass(pitchclass)) == f"<PitchClass: {pitchnames}, scale: None>"
    for pitchname in data_pitchname:
        assert str(PitchClass(pitchname)) == f"<PitchClass: {pitchname}, scale: None>"
