"""音価・拍子・周期リズムと、直列・並列の構造."""

from fractions import Fraction

from aulos.rhythm import Cycle
from aulos.rhythm import Duration
from aulos.rhythm import Event
from aulos.rhythm import Meter
from aulos.rhythm import Tempo
from aulos.western.equal import Chord
from aulos.western.equal import Pitch

quarter = Duration(Fraction(1, 4))
eighth = Duration(Fraction(1, 8))

# 小節の長さが同じでも、分割の順序で拍の強弱が変わる。
print("6/8", Meter((2, 3), eighth).weights)
print("3/4", Meter((3, 2), eighth).weights)

# 8パルスに3打点を最も均等に置いた型と、5度の連鎖から作る七音音階は同じ構造を持つ。
tresillo = Cycle.euclidean(8, 3)
print(tresillo.onsets, tresillo.steps, Cycle.generated(12, 7, 7).mode(4).steps)
print("3:4", (Cycle.euclidean(3, 3) | Cycle.euclidean(4, 4)).onsets)

# 直列は+、並列は|で合成する。長さは直列で和、並列で最大値になる。
melody = Event(quarter, Pitch("E4")) + Event(eighth) + Event(eighth, Pitch("G4")) + Event(quarter * 2, Pitch("C5"))
harmony = Event(quarter * 4, Chord("C/E"))
phrase = melody | harmony
print(phrase.duration.value, melody.duration.value)

# 記譜上の時刻は有理数のまま保ち、秒への評価はテンポに任せる。
tempo = Tempo(quarter, 120.0)
meter = Meter((2, 2, 2), eighth)
for placed in melody.events():
    seconds = tempo.seconds(placed.start - meter.position(0))
    print(
        placed.value, placed.start.value, meter.level(placed.start), seconds, placed.value.frequency(Pitch("A4"), 440.0)
    )
