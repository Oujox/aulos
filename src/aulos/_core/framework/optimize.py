import typing as t
from typing import ClassVar


class OptimizedMeta(type):
    def __new__(cls, name: str, bases: tuple[type], dct: dict[str, t.Any], **kwargs):
        annotations: dict[str, type] = dct.get("__annotations__", {})
        slots = tuple(
            name
            for name, typ in annotations.items()
            if not (hasattr(typ, "__origin__") and typ.__origin__ is ClassVar)
        )
        dct["__slots__"] = slots
        return super(OptimizedMeta, cls).__new__(cls, name, bases, dct, **kwargs)
