"""調律を束ねない五文字の記譜体系."""

from fractions import Fraction

from aulos.base import Temperament
from aulos.base import Tuning
from aulos.pentatonic import Pitch
from aulos.pentatonic import Scale

scale = Scale("a natural")
print(scale.names, scale.chord().names)

# 調律を束ねていないので、周波数の評価には調律の指定が必要になる。
tuning = Tuning(Temperament.equal_division((2, 3), 5, Fraction(2)), (240.0,))
print(scale.frequencies(Pitch("a4"), 440.0, tuning))
