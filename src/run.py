import os
import pathlib

from aulos import *
from aulos.scale import *

path = pathlib.Path(os.path.dirname(__file__)) / "setting.toml"

with Context.from_toml(path) as c:
    from pprint import pprint

    for k in c.schema.pitchnames:
        if len(k) <= 2:
            pprint(Locrian(Key("Fb")).diatonics)
