import typing as t


class SlotsGenerateMeta(type):
    """
    SlotsGenerateMeta is a metaclass that automatically generates __slots__ for classes.

    This metaclass inspects the class annotations and generates a __slots__ attribute
    based on the annotated attributes, excluding those marked as ClassVar or type.
    This helps in reducing memory usage and improving attribute access speed for instances
    of the class.

    Attributes:
        slots_generate (bool): A flag to enable or disable the automatic generation of __slots__.
    """

    def __new__(
        cls,
        name: str,
        bases: tuple[type, ...],
        namespace: dict[str, t.Any],
        *,
        slots_generate: bool = True,
        **kwargs: t.Any,
    ) -> "SlotsGenerateMeta":
        if slots_generate and not namespace.get("__slots__", False):
            annotations: dict[str, type] = namespace.get("__annotations__", {})
            slots = tuple(
                name
                for name, typ in annotations.items()
                if not (hasattr(typ, "__origin__") and t.get_origin(typ) is t.ClassVar)
                if not (hasattr(typ, "__origin__") and t.get_origin(typ) is type)
            )
            namespace["__slots__"] = slots
        return super().__new__(cls, name, bases, namespace, **kwargs)
