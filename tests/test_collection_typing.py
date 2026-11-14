from typing import TYPE_CHECKING
from typing import assert_type

from aulos.base import Chord as BaseChord
from aulos.base import Interval
from aulos.base import Notation
from aulos.western import WesternTag
from aulos.western.equal import Chord
from aulos.western.equal import Scale

if TYPE_CHECKING:
    from aulos.pentatonic import Chord as OtherChord
    from aulos.pentatonic import PentatonicTag


def test_public_definitions_preserve_classification_types():
    assert_type(Chord.notation, Notation[WesternTag])
    assert_type(Scale.notation, Notation[WesternTag])
    assert_type(Chord.notation.interval(1), Interval[WesternTag])
    assert_type(Chord.tag, type[WesternTag])
    assert_type(Scale("C major").chord(), BaseChord[WesternTag])


if TYPE_CHECKING:
    # unused-ignore-commentをエラーにして検査し、異分類の拒否も静的に保証する。
    class WrongDefinition(BaseChord[WesternTag], abstract=True):
        notation = OtherChord.notation  # ty: ignore[invalid-assignment]
        tag = PentatonicTag  # ty: ignore[invalid-assignment]

    Chord("C").transpose(OtherChord.notation.interval(1))  # ty: ignore[invalid-argument-type]
