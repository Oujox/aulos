import typing as t


class InstanceCacheMeta(type):

    _instance_cache: t.ClassVar[dict[tuple[tuple, frozenset], t.Any]]

    def __new__(cls, name: str, bases: tuple[type], dct: dict[str, t.Any], **kwargs):
        dct["_instance_cache"] = {}
        return super(InstanceCacheMeta, cls).__new__(cls, name, bases, dct, **kwargs)

    def __call__(cls, *args, **kwargs):
        key = (args, frozenset(kwargs.items()))
        if key not in cls._instance_cache:
            cls._instance_cache[key] = super(InstanceCacheMeta, cls).__call__(
                *args, **kwargs
            )
        return cls._instance_cache[key]
