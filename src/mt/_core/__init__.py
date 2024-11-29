"""Core
---
* settingに必要な仕組みの提供
"""

# utils
# interfaces
from . import context, interfaces, utils
# implementation
from .object import Object
from .setting import Setting

__all__ = ["Object", "Setting", "interfaces", "context", "utils"]
