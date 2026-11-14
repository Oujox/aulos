"""19平均律と1/4コンマ・ミーントーンでの評価.

同じ綴りの和音を、束ねた調律の代わりに引数の調律で評価する。
"""

from fractions import Fraction
from math import log2

from aulos.base import Temperament
from aulos.base import Tuning
from aulos.western.equal import Chord
from aulos.western.equal import Pitch

chord = Chord("C")
a4 = Pitch("A4")

nineteen = Tuning(Temperament.equal_division((2, 3, 5), 19, Fraction(2)), (1200 / 19,))
print("19-EDO", chord.frequencies(a4, 440.0, nineteen))

# 生成音程はオクターブと5度。5は4個の5度から2オクターブ引いた位置に写る。
meantone_map = Temperament((2, 3, 5), ((1, 1, 0), (0, 1, 4)))
meantone = Tuning(meantone_map, (1200.0, 1200 * log2(5) / 4))
print("meantone", chord.frequencies(a4, 440.0, meantone))
print("81/80 tempered out:", meantone_map.tempers_out(Fraction(81, 80)))
