import pytest

from src.euterpe import Setting

SETTING_DICT_FOR_HSYS12 = {
    "pitchclass": {
        "intervals": [2, 2, 1, 2, 2, 2, 1],
        "symbols": ["C", "D", "E", "F", "G", "A", "B"],
        "accidental": {
            "limit": 2,
            "symbol": {"sharp": "#", "flat": "b", "nature": "n"},
        },
    },
    "note": {
        "notenumber": {"min": 0, "max": 127},
        "presentation": {
            "symbols": [
                "<N>-1",
                "<N>0",
                "<N>1",
                "<N>2",
                "<N>3",
                "<N>4",
                "<N>5",
                "<N>6",
                "<N>7",
                "<N>8",
                "<N>9",
            ],
            "reference": {"number": 60, "symbol": "<N>4"},
        },
        "tuner": {"reference": {"hz": 440, "number": 69}},
    },
}


@pytest.fixture(params=[SETTING_DICT_FOR_HSYS12], scope="session")
def setting(request) -> Setting:
    return Setting.from_dict(request.param)


@pytest.fixture(scope="module")
def data_pitchclass(setting) -> list[int]:
    return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


@pytest.fixture(scope="module")
def data_pitchname(setting) -> list[str]:
    return [
        "Abb",
        "Ab",
        "A",
        "A#",
        "A##",
        "Bbb",
        "Bb",
        "B",
        "B#",
        "B##",
        "Cbb",
        "Cb",
        "C",
        "C#",
        "C##",
        "Dbb",
        "Db",
        "D",
        "D#",
        "D##",
        "Ebb",
        "Eb",
        "E",
        "E#",
        "E##",
        "Fbb",
        "Fb",
        "F",
        "F#",
        "F##",
        "Gbb",
        "Gb",
        "G",
        "G#",
        "G##",
    ]


@pytest.fixture(scope="module")
def data_map_pitchclass_to_pitchnames(setting) -> dict[int, str | None]:
    return {
        0: ("Dbb", None, "C", "B#", None),
        1: (None, "Db", None, "C#", "B##"),
        2: ("Ebb", None, "D", None, "C##"),
        3: ("Fbb", "Eb", None, "D#", None),
        4: (None, "Fb", "E", None, "D##"),
        5: ("Gbb", None, "F", "E#", None),
        6: (None, "Gb", None, "F#", "E##"),
        7: ("Abb", None, "G", None, "F##"),
        8: (None, "Ab", None, "G#", None),
        9: ("Bbb", None, "A", None, "G##"),
        10: ("Cbb", "Bb", None, "A#", None),
        11: (None, "Cb", "B", None, "A##"),
    }


@pytest.fixture(scope="module")
def data_map_pitchname_to_pitchclass(setting) -> dict[str, int]:
    return {
        "Dbb": 0,
        "C": 0,
        "B#": 0,
        "Db": 1,
        "C#": 1,
        "B##": 1,
        "Ebb": 2,
        "D": 2,
        "C##": 2,
        "Fbb": 3,
        "Eb": 3,
        "D#": 3,
        "Fb": 4,
        "E": 4,
        "D##": 4,
        "Gbb": 5,
        "F": 5,
        "E#": 5,
        "Gb": 6,
        "F#": 6,
        "E##": 6,
        "Abb": 7,
        "G": 7,
        "F##": 7,
        "Ab": 8,
        "G#": 8,
        "Bbb": 9,
        "A": 9,
        "G##": 9,
        "Cbb": 10,
        "Bb": 10,
        "A#": 10,
        "Cb": 11,
        "B": 11,
        "A##": 11,
    }
