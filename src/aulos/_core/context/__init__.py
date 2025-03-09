"""
Context Module
-------------

Provides context management and dependency injection for Aulos objects.
Includes Context class for managing application state and inject decorator
for automatic dependency resolution.
"""

from .context import Context
from .inject import inject

__all__ = ["Context", "inject"]
