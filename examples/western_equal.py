"""12平均律の音高・和音・音階・根音なしの音程列."""

from fractions import Fraction

from aulos.western.equal import Chord
from aulos.western.equal import Pitch
from aulos.western.equal import Scale
from aulos.western.equal import Voicing

a4 = Pitch("A4")

pitch = Pitch("C#4")
print(pitch, pitch.pitch_class, pitch.frequency(a4, 440.0))

chord = Chord("Cm7")
print(chord, chord.names, chord.frequencies(a4, 440.0))

fifth = chord.notation.interval(Fraction(3, 2))
print(chord.transpose(fifth).names)

scale = Scale("C major")
print(scale.names)
print(scale.mode(1), scale.chord(1, count=4).names)
print([str(Scale("C melodic minor").mode(index)) for index in range(7)])

# 登録済みの名前は templates.names で一覧できる。別名(CM7、C-7 など)は同じ構造を返す。
print(Chord.templates.names)
print(Chord("CM7"), Chord("C-7"), Chord("C7#9").names)

print([str(member) for member in Voicing("m7").at(Pitch("D4"))])
