from euterpe import *
from euterpe.scale import *
from euterpe.utils import *
from euterpe.tuner import *

euterpe = Euterpe("my")

@euterpe.WorkSpace()
def track1():
    from pprint import pprint

    ab5 = Chord("Abbm7(b5)/E")
    print(ab5.root, ab5.quality.name, ab5.on)

    pprint(Tuner.mro())
    pprint(Dorian(Key("C")).diatonics)
    pprint(PitchClass(2, scale=Locrian(Key("C"))))

track1()