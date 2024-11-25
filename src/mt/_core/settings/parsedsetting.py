from dataclasses import dataclass

from .notenumber import NoteNumberSetting
from .scheme import SchemeSetting


@dataclass(frozen=True)
class ParsedSetting:
    scheme: SchemeSetting
    notenumber: NoteNumberSetting
