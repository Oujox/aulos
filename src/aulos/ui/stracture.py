import typing as t
from argparse import Namespace
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class CommandResult(Namespace):
    execute: t.Callable[[t.Self], None] = field(init=False)
