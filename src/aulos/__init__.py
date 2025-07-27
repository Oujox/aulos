"""
Aulos Library Initialization
----------------------------

This module initializes the Aulos library, a Python package designed for speech processing and
analysis from a music theory perspective. It imports essential components and modules, making
them available for use in the library.

Modules and Classes:
- TET12, TET24: Modules for handling 12-tone and 24-tone equal temperament systems.
- Setting: Core settings management for the library.

The `__all__` list defines the public API of the module, specifying which components
are accessible when the module is imported.
"""

from . import TET12, TET24
from ._core import BaseScale, BaseTuner, Setting
from ._errors import *  # noqa: F403
from ._warnings import *  # noqa: F403

__all__ = [
    "TET12",
    "TET24",
    "BaseScale",
    "BaseTuner",
    "Setting",
]
