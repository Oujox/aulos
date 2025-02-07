"""
Aulos Library Initialization
----------------------------

This module initializes the Aulos library, a Python package designed for speech processing and
analysis from a music theory perspective. It imports essential components and modules, making
them available for use in the library.

Modules and Classes:
- TET12, TET24: Modules for handling 12-tone and 24-tone equal temperament systems.
- Setting: Core settings management for the library.
- BaseKey, BaseNote, BasePitchClass: Fundamental classes for musical keys, notes, and pitch classes.
- DiatonicScale, NondiatonicScale, Scale: Classes for representing musical scales.
- Tuner: Class for tuning systems.
- _errors, _warnings: Modules for handling errors and warnings.

The `__all__` list defines the public API of the module, specifying which components
are accessible when the module is imported.
"""

from . import TET12, TET24
from ._core import Setting
from ._errors import *  # noqa: F403
from ._warnings import *  # noqa: F403
from .note import BaseKey, BaseNote, BasePitchClass
from .scale import DiatonicScale, NondiatonicScale, Scale
from .tuner import Tuner

__all__ = [
    "TET12",
    "TET24",
    "BaseKey",
    "BaseNote",
    "BasePitchClass",
    "DiatonicScale",
    "NondiatonicScale",
    "Scale",
    "Setting",
    "Tuner",
]
