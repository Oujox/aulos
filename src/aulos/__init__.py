""" aulos (library for music theory)
"""

from . import scale, tuner, utils
from ._core import Setting
from ._errors import *
from ._version import *
from ._warnings import *
from .chord import *
from .note import Key, PitchClass

__all__ = ["PitchClass", "Key", "Setting", "scale", "tuner", "utils"]
