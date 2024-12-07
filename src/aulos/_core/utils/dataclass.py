import typing as t
from dataclasses import is_dataclass, fields, dataclass
from functools import update_wrapper


def from_dict[T](cls: type[T], value: dict[str, t.Any]) -> T:
    # 1. Check if the provided class is a dataclass
    if not is_dataclass(cls):
        raise ValueError(f"The provided class {cls.__name__} is not a dataclass type.")

    # 2. Convert list type in dictionary to tuple type
    # 3. Recursively convert dict to dataclass
    init_dict = {}
    dfields_type = {f.name: f.type for f in fields(cls)}
    dfields_init = {f.name: f.init for f in fields(cls)}

    for k, v in value.items():
        if k in dfields_type:
            # no initialize parameter
            if not dfields_init[k]:
                continue
            # initialize parameter
            if isinstance(v, dict):
                init_dict[k] = from_dict(dfields_type[k], v)
            elif isinstance(v, list):
                init_dict[k] = tuple(v)
            else:
                init_dict[k] = v

    return cls(**init_dict)


def initializer(cls):

    class _:
        def aiueo(self) -> int: ...

    setattr(cls, from_dict.__class__.__name__, from_dict)
    update_wrapper(from_dict, cls)
    return cls


class _:
    def aiueo(self) -> int: ...


@initializer
class A: ...


A()
