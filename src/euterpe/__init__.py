""" euterpe (library for music theory)
"""

from ._core import Setting
from ._errors import *
from ._version import *
from ._warnings import *
from .note import _Key
from .note import _Note
from .note import _PitchClass
from .scale import _Scale
from .scale import _DiatonicScale
from .scale import _NondiatonicScale
from .tuner import _Tuner

# implements
from . import TET12


__all__ = [
    "_PitchClass",
    "_Key",
    "_Note",
    "_Scale",
    "_DiatonicScale",
    "_NondiatonicScale",
    "_Tuner",
    "Setting",
    "TET12",
]
