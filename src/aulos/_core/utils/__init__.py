"""
Utils Module
-----------

Core utility functions and tools independent of Aulos implementation.
Provides generic helpers for intervals, positions, indexing, and type operations.
"""

from .dataclass import from_dict
from .property import classproperty
from .representation import Intervals, Positions
from .sequence import index, rotated

__all__ = [
    "Intervals",
    "Positions",
    "classproperty",
    "from_dict",
    "index",
    "rotated",
]
