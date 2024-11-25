import os
import pathlib

from mt import *
from mt.scale import *

path = pathlib.Path(os.path.dirname(__file__)) / "setting.toml"

with Context(path) as c:

    for k in c.setting.get().scheme.pitchnames:
        if len(k) <= 2:
            print(k, Dorian(Key(k)).diatonics)
