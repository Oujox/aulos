from aulos import *
from aulos.scale import *
from aulos.utils import *

with Aulos() as a:
    from pprint import pprint

    # print(a.internal.get().get("setting").note.derive.name2number)
    pprint(Major(Key("C")).diatonics)
    pprint(Locrian(Key("C")))
    PitchClass(0, scale=Locrian(Key("C")))
