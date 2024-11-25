"""Core
---
* settingに必要な仕組みの提供
* 具体的な理論のためのデータ構造・仕組みは扱わない ⇒ shared
"""

# utils
# interfaces
from . import context, interfaces, utils

# implementation
from .object import ObjectMT
from .setting import SettingMT

__all__ = ["ObjectMT", "SettingMT", "interfaces", "context", "utils"]
