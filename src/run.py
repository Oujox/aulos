from euterpe.utils import *
from euterpe.TET_12 import *


euterpe = Euterpe("my")

@euterpe.WorkSpace()
def workspace():
    from pprint import pprint

    # ab5 = Chord("Abm7(b5)/E")
    # print(ab5.root, ab5.quality.name, ab5.on)

    # pprint(Dorian_s4.mro())
    print(Note(70, tuner=JustIntonationTuner(440)).hz)
    print(Note(70, tuner=Equal12Tuner(440)).hz)
    print(Note(70, tuner=MeantoneTuner(440)).hz)
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
    print(Key.schema.pitchclass.count_accidental("F#"))
    print(MinorPentatonic.PitchClass)
    pprint(Aeorian(Key("C")).components)

    # for key in Note("C#4").schema.pitchnames:
    #     if len(key) < 3:
    #         print(key)
    #         pprint(Pentatonic(Key(key)).components)

workspace()