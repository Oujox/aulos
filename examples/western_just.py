"""5リミット純正律の綴りと周波数."""

from aulos.western.just import Chord
from aulos.western.just import Pitch

chord = Chord("Cm7")
print(chord.names)
print([str(interval.ratio()) for interval in chord.intervals])
print(chord.frequencies(chord.root, 261.626))

# シントニック・コンマの分だけ異なる綴りは別の音高になる。
print(Pitch("A4") == Pitch("A4↓"), (Pitch("A4") - Pitch("A4↓")).ratio())
