from __future__ import annotations

from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from ...setting import Setting
    from ..note import NoteSetting


@dataclass(frozen=True, init=False)
class NoteSettingDerive:
    def __init__(self, setting: Setting): ...
