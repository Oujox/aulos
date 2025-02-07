import typing as t
from typing import ClassVar


class OptimizedMeta(type):
    """
    OptimizedMeta is a metaclass that optimizes class creation by automatically
    generating __slots__ based on type annotations, excluding ClassVar and type annotations.

    Methods:
        __new__(cls, name, bases, namespace, **kwargs):
            Creates a new class with optimized __slots__ if not explicitly defined.
    """

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, t.Any],
        /,
        **kwargs: t.Any,
    ) -> "OptimizedMeta":
        if not namespace.get("__slots__"):
            annotations: dict[str, type] = namespace.get("__annotations__", {})
            slots = tuple(
                name
                for name, typ in annotations.items()
                if not (hasattr(typ, "__origin__") and t.get_origin(typ) is ClassVar)
                if not (hasattr(typ, "__origin__") and t.get_origin(typ) is type)
            )
            namespace["__slots__"] = slots
        return super().__new__(cls, name, bases, namespace, **kwargs)
