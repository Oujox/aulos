from euterpe import *
from euterpe.scale import *
from euterpe.utils import *
from euterpe.tuner import *

euterpe = Euterpe("my")

@euterpe.WorkSpace()
def track1():
    from pprint import pprint

    # ab5 = Chord("Abbm7(b5)/E")
    # print(ab5.root, ab5.quality.name, ab5.on)

    # pprint(Tuner.mro())
    # pprint(Dorian(Key("C")).components)
    # pprint(Dorian(Key("F#")).components)
    # pprint(Dorian(Key("Gb")).components)
    

    # pprint(Pentatonic.intervals)
    # pprint(Pentatonic.positions)
    # pprint(Pentatonic(Key("Gb")).accidentals)
    # pprint(Pentatonic(Key("Gb")).components)
    # pprint(MinorPentatonic.intervals)
    # pprint(MinorPentatonic.positions)
    # pprint(Ionian(Key("F#")).accidentals)
    # pprint(Pentatonic(Key("F#")).components)
    # pprint(MinorPentatonic(Key("F#")).components)

    for key in Note("C#4").schema.pitchnames:
        if len(key) < 3:
            print(key)
            pprint(Wholetone(Key(key)).components)

track1()