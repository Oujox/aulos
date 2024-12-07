import os
import pathlib

from aulos import *
from aulos.scale import *
from aulos.utils import *

path = pathlib.Path(os.path.dirname(__file__)) / "setting.toml"
setting = Setting.from_toml(path)

with Aulos(setting=setting):
    from pprint import pprint

    pprint(Locrian(Key("Fb")).diatonics)
