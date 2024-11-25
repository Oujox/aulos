import pytest
from src.mt import SettingMT


SETTING_DICT_FOR_HSYS12 = {
    "scheme": {
        "semitone": 12,
        "intervals": [2, 1, 2, 2, 1, 2, 2],
        "symbols": ["A", "B", "C", "D", "E", "F", "G"],
        "accidental": {"limit": 2, "upper_symbol": "#", "lower_symbol": "b"},
    },
    "notenumber": {
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


@pytest.fixture(params=[SETTING_DICT_FOR_HSYS12])
def setting(request) -> SettingMT:
    return SettingMT(request.param)


@pytest.fixture
def data_pitchnames() -> list[str]:
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


@pytest.fixture
def data_pitchclasses() -> list[int]:
    return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


@pytest.fixture
def data_invalid_pitchnames() -> str:
    return ["a"]
