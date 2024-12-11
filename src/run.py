import os
import pathlib

from aulos import *
from aulos.scale import *
from aulos.utils import *

path = pathlib.Path(os.path.dirname(__file__)) / "setting.toml"
setting = Setting.from_toml(path)

with Aulos(setting=setting) as a:
    from pprint import pprint

    # print(a.internal.get().get("setting").note.derive.name2number)
    # pprint(Major(Key("C")).diatonics)
    # pprint(Locrian(Key("C")).diatonics)
    print(Note(60, scale=Locrian(Key("C"))) + 3)
