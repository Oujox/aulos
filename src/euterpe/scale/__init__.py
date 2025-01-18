""" Scale
---
This module provides a collection of music theory tools for working with scales and modes.
It includes diatonic and nondiatonic scales, as well as several modes derived from both the 
major, harmonic minor, and melodic minor scales. These scales and modes are useful for 
composition, music analysis, and algorithmic music generation.
"""

from . import schemas
from .diatonic import _DiatonicScale, _NondiatonicScale
from .scale import _Scale

__all__ = [
    "_Scale",
    "_DiatonicScale",
    "_NondiatonicScale",
    "schemas",
]
