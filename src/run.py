from aulos import *
from aulos.scale import *
from aulos.utils import *

with Aulos(enable_coexistence_check=True) as a:
    from pprint import pprint

    # print(a.internal.get().get("setting").note.derive.name2number)
    pprint(Major(Key("C")).diatonics)
    pprint(Locrian(Key("C")).diatonics)
    print(PitchClass(0, scale=Locrian(Key("C"))) + 3)
    print(Note(60, scale=Locrian(Key("C"))) + 3)
