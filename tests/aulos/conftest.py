import pytest
from dacite import from_dict

from src.aulos import Setting

SETTING_DICT_FOR_HSYS12 = {
    "pitchclass": {
        "semitone": 12,
        "intervals": [2, 1, 2, 2, 1, 2, 2],
        "symbols": ["A", "B", "C", "D", "E", "F", "G"],
        "accidental": {"limit": 2, "upper_symbol": "#", "lower_symbol": "b"},
    },
    "note": {
        "min": 0,
        "max": 128,
        "presentations": [
            {
                "name": "scientific pitch notation",
                "areas": "SPN",
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
                "reference": {"number": 69, "symbol": 6},
            },
            {
                "name": "helmholtz pitch notation",
                "areas": "HPN",
                "symbols": [
                    "<N>,,,",
                    "<N>,,",
                    "<N>,",
                    "<N>",
                    "<n>'",
                    "<n>''",
                    "<n>'''",
                    "<n>''''",
                    "<n>'''''",
                    "<n>''''''",
                    "<n>'''''''",
                ],
                "reference": {"number": 69, "symbol": 4},
            },
        ],
    },
}


@pytest.fixture(params=[SETTING_DICT_FOR_HSYS12], scope="session")
def setting(request) -> Setting:
    return from_dict(Setting, request.param)


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
        0: ["Bbb", None, "A", None, "G##"],
        1: ["Cbb", "Bb", None, "A#", None],
        2: [None, "Cb", "B", None, "A##"],
        3: ["Dbb", None, "C", "B#", None],
        4: [None, "Db", None, "C#", "B##"],
        5: ["Ebb", None, "D", None, "C##"],
        6: ["Fbb", "Eb", None, "D#", None],
        7: [None, "Fb", "E", None, "D##"],
        8: ["Gbb", None, "F", "E#", None],
        9: [None, "Gb", None, "F#", "E##"],
        10: ["Abb", None, "G", None, "F##"],
        11: [None, "Ab", None, "G#", None],
    }


@pytest.fixture(scope="module")
def data_map_pitchname_to_pitchclass(setting) -> dict[str, int]:
    return {
        "Abb": 10,
        "Ab": 11,
        "A": 0,
        "A#": 1,
        "A##": 2,
        "Bbb": 0,
        "Bb": 1,
        "B": 2,
        "B#": 3,
        "B##": 4,
        "Cbb": 1,
        "Cb": 2,
        "C": 3,
        "C#": 4,
        "C##": 5,
        "Dbb": 3,
        "Db": 4,
        "D": 5,
        "D#": 6,
        "D##": 7,
        "Ebb": 5,
        "Eb": 6,
        "E": 7,
        "E#": 8,
        "E##": 9,
        "Fbb": 6,
        "Fb": 7,
        "F": 8,
        "F#": 9,
        "F##": 10,
        "Gbb": 8,
        "Gb": 9,
        "G": 10,
        "G#": 11,
        "G##": 0,
    }
