"""Core
---
* settingに必要な仕組みの提供
"""

# utils, framework
from . import framework, utils
# implementation
from .object import AulosObject
from .setting import Setting

__all__ = ["AulosObject", "Setting", "framework", "utils"]
