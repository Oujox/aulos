from euterpe import *
from euterpe.scale import *
from euterpe.utils import *
from euterpe.tuner import *

euterpe = Euterpe("my")

@euterpe.WorkSpace()
def workspace():
    from pprint import pprint

    # ab5 = Chord("Abm7(b5)/E")
    # print(ab5.root, ab5.quality.name, ab5.on)

    # pprint(Dorian_s4.mro())
    print(Note(70, tuner=JustIntonationTuner()).hz)
    print(Note(70, tuner=Equal12Tuner()).hz)
    print(Note(70, tuner=MeantoneTuner()).hz)
    # pprint(Dorian(Key("F#")).signatures)
    # pprint(Locrian(Key("C")).components)
    

    # pprint(Pentatonic.intervals)
    # pprint(Pentatonic.positions)
    # pprint(Pentatonic(Key("Gb")).signatures)
    # pprint(Pentatonic(Key("Gb")).components)
    # pprint(MinorPentatonic.intervals)
    # pprint(MinorPentatonic.positions)
    # pprint(Ionian(Key("F#")).signatures)
    # pprint(Locrian_n6(Key("F#")).components)
    pprint(MinorPentatonic(Key("F#")).components)

    # for key in Note("C#4").schema.pitchnames:
    #     if len(key) < 3:
    #         print(key)
    #         pprint(Pentatonic(Key(key)).components)

workspace()