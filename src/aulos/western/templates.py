"""西洋式の和音・音階の綴り付きテンプレート。調律や純正比は指定しない.

構造は ``"1 b3 5 b7"`` のように、長音階の度数と変化記号で書く。
同じ構造の別名は入力でだけ受け付け、表示には先頭の名前を使う。
"""

from aulos.base import ChainInterval
from aulos.base import Template
from aulos.base import Templates


def _degree(text: str) -> ChainInterval:
    """``"b3"`` や ``"#11"`` のような、長音階の度数と変化記号を連鎖変位にする。複音程にも対応する."""
    number = text.lstrip("#b")
    alteration = text.count("#") - text.count("b")
    turns, position = divmod(int(number) - 1, 7)
    generators = (0, 2, 4, -1, 1, 3, 5)[position]
    periods = (0, -1, -2, 1, 0, -1, -2)[position]
    return ChainInterval(generators + alteration * 7, periods + turns - alteration * 4)


def _templates(*entries: tuple[str, ...]) -> Templates:
    """``(度数列, 名前, 別名...)`` の並びからテンプレート集を作る."""
    return Templates(
        tuple(
            Template(name, tuple(_degree(degree) for degree in degrees.split()), tuple(aliases))
            for degrees, name, *aliases in entries
        )
    )


chords = _templates(
    # 三和音と二音
    ("1 3 5", "", "maj", "M"),
    ("1 b3 5", "m", "min", "-"),
    ("1 b3 b5", "dim"),
    ("1 3 #5", "aug", "+"),
    ("1 2 5", "sus2"),
    ("1 4 5", "sus4", "sus"),
    ("1 5", "5"),
    # 付加音
    ("1 3 5 6", "6"),
    ("1 b3 5 6", "m6"),
    ("1 3 5 6 9", "69"),
    ("1 b3 5 6 9", "m69"),
    ("1 3 5 9", "add9"),
    ("1 b3 5 9", "madd9"),
    ("1 3 5 11", "add11"),
    # 七の和音
    ("1 3 5 b7", "7"),
    ("1 3 5 7", "maj7", "M7"),
    ("1 b3 5 b7", "m7", "min7", "-7"),
    ("1 b3 5 7", "mMaj7", "mM7"),
    ("1 b3 b5 bb7", "dim7"),
    ("1 b3 b5 b7", "m7b5"),
    ("1 3 #5 b7", "aug7", "7#5", "+7"),
    ("1 3 #5 7", "augMaj7", "maj7#5"),
    ("1 3 b5 b7", "7b5"),
    ("1 4 5 b7", "7sus4", "7sus"),
    ("1 2 5 b7", "7sus2"),
    # 九・十一・十三の和音
    ("1 3 5 b7 9", "9"),
    ("1 3 5 7 9", "maj9", "M9"),
    ("1 b3 5 b7 9", "m9", "min9", "-9"),
    ("1 b3 5 7 9", "mMaj9", "mM9"),
    ("1 4 5 b7 9", "9sus4", "9sus"),
    ("1 3 5 b7 9 11", "11"),
    ("1 3 5 7 9 11", "maj11", "M11"),
    ("1 b3 5 b7 9 11", "m11", "min11", "-11"),
    ("1 3 5 b7 9 11 13", "13"),
    ("1 3 5 7 9 11 13", "maj13", "M13"),
    ("1 b3 5 b7 9 11 13", "m13", "min13", "-13"),
    # 変化したテンション
    ("1 3 5 b7 b9", "7b9"),
    ("1 3 5 b7 #9", "7#9"),
    ("1 3 5 b7 #11", "7#11"),
    ("1 3 5 b7 b13", "7b13"),
    ("1 3 5 b7 b9 b13", "7b9b13"),
    ("1 3 5 b7 #9 b13", "7#9b13"),
    ("1 3 5 b7 9 #11", "9#11"),
    ("1 3 5 b7 9 #11 13", "13#11"),
    ("1 3 5 7 #11", "maj7#11", "M7#11"),
    ("1 3 5 7 9 #11", "maj9#11", "M9#11"),
)

scales = _templates(
    # 全音階の旋法
    ("1 2 3 4 5 6 7", "major", "ionian"),
    ("1 2 b3 4 5 b6 b7", "minor", "natural minor", "aeolian"),
    ("1 2 b3 4 5 6 b7", "dorian"),
    ("1 b2 b3 4 5 b6 b7", "phrygian"),
    ("1 2 3 #4 5 6 7", "lydian"),
    ("1 2 3 4 5 6 b7", "mixolydian"),
    ("1 b2 b3 4 b5 b6 b7", "locrian"),
    # 和声的短音階とその旋法
    ("1 2 b3 4 5 b6 7", "harmonic minor"),
    ("1 b2 b3 4 b5 6 b7", "locrian #6"),
    ("1 2 3 4 #5 6 7", "ionian #5"),
    ("1 2 b3 #4 5 6 b7", "dorian #4"),
    ("1 b2 3 4 5 b6 b7", "phrygian dominant"),
    ("1 #2 3 #4 5 6 7", "lydian #2"),
    ("1 b2 b3 b4 b5 b6 bb7", "ultralocrian"),
    # 旋律的短音階とその旋法
    ("1 2 b3 4 5 6 7", "melodic minor"),
    ("1 b2 b3 4 5 6 b7", "dorian b2"),
    ("1 2 3 #4 #5 6 7", "lydian augmented"),
    ("1 2 3 #4 5 6 b7", "lydian dominant"),
    ("1 2 3 4 5 b6 b7", "mixolydian b6"),
    ("1 2 b3 4 b5 b6 b7", "locrian #2"),
    ("1 b2 b3 b4 b5 b6 b7", "altered", "super locrian"),
    # その他の七音音階
    ("1 2 3 4 5 b6 7", "harmonic major"),
    ("1 b2 3 4 5 b6 7", "double harmonic"),
    ("1 2 b3 #4 5 b6 7", "hungarian minor"),
    ("1 #2 3 #4 5 6 b7", "hungarian major"),
    ("1 b2 b3 4 5 b6 7", "neapolitan minor"),
    ("1 b2 b3 4 5 6 7", "neapolitan major"),
    # 五音音階とブルース
    ("1 2 3 5 6", "major pentatonic"),
    ("1 b3 4 5 b7", "minor pentatonic"),
    ("1 b3 4 b5 5 b7", "blues", "minor blues"),
    ("1 2 b3 3 5 6", "major blues"),
    ("1 2 b3 5 b6", "hirajoshi"),
    ("1 b2 4 5 b6", "in"),
    ("1 b2 4 5 b7", "insen"),
    ("1 2 4 5 6", "yo"),
    ("1 3 4 5 7", "ryukyu"),
    # 対称的な音階と経過音を持つ音階
    ("1 2 3 #4 #5 b7", "whole tone"),
    ("1 b3 3 5 #5 7", "augmented"),
    ("1 2 b3 4 b5 b6 6 7", "diminished"),
    ("1 b2 b3 3 #4 5 6 b7", "dominant diminished"),
    ("1 2 3 4 5 6 b7 7", "bebop dominant"),
    ("1 2 3 4 5 b6 6 7", "bebop major"),
    ("1 b2 2 b3 3 4 #4 5 b6 6 b7 7", "chromatic"),
)
