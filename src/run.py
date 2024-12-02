import os
import pathlib

from aulos import *
from aulos.scale import *

path = pathlib.Path(os.path.dirname(__file__)) / "setting.toml"

with Context.from_toml(path) as c:
    from pprint import pprint

    pprint(Scale.mro())

    for k in c.scheme.pitchnames:
        if len(k) <= 2:
            pprint(Locrian(Key(k)).diatonics)
