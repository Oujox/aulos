from aulos import *
from aulos.scale import *
from aulos.utils import *
from aulos.tuner import *

with Aulos():
    from pprint import pprint

    pprint(Major(Key("C")))
    pprint(Dorian(Key("C")).diatonics)
    pprint(PitchClass(2, scale=Locrian(Key("C"))))
