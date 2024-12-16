from aulos import *
from aulos.scale import *
from aulos.utils import *
from aulos.tuner import *

with Aulos():
    from pprint import pprint

    ab5 = Chord("Am7(b5)/E")
    print(ab5.root, ab5.quality.name, ab5.on)

    pprint(Tuner.mro())
    pprint(Dorian(Key("C")).diatonics)
    pprint(PitchClass(2, scale=Locrian(Key("C"))))
