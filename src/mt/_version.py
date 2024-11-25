import sys
import warnings

REQUIRED_PYTHON_VERSION = (3, 12)

if sys.version_info < REQUIRED_PYTHON_VERSION:
    warnings.warn(
        f"Your Python version is {sys.version_info.major}.{sys.version_info.minor}. "
        f"This module requires Python {REQUIRED_PYTHON_VERSION[0]}.{REQUIRED_PYTHON_VERSION[1]}.",
        RuntimeWarning,
    )

__all__ = []
