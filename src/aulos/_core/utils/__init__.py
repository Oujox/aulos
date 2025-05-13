"""
Utils Module
-----------

Core utility functions and tools independent of Aulos implementation.
Provides generic helpers for intervals, positions, indexing, and type operations.
"""

from .dataclass import from_dict
from .intervals import Intervals
from .positions import Positions
from .property import classproperty
from .sequence import index

__all__ = [
    "Intervals",
    "Positions",
    "classproperty",
    "from_dict",
    "index",
]
