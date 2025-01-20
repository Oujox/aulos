import typing as t


class DerivedCacheMeta(type):

    _derived_cache: t.ClassVar[list[type]]

    def __new__(cls, name: str, bases: tuple[type], dct: dict[str, t.Any], **kwargs):
        dct["_derived_cache"] = []
        return super(DerivedCacheMeta, cls).__new__(cls, name, bases, dct, **kwargs)

    def __init__(cls, name: str, bases: tuple[type], dct: dict[str, t.Any], **kwargs):
        super().__init__(name, bases, dct)
        for base in bases:
            if isinstance(base, DerivedCacheMeta):
                base._derived_cache.append(cls)
