import typing as t
from functools import wraps

from .context import Context


class InjectedMeta(type):
    def __new__(cls, name: str, bases: tuple[type], dct: dict[str, t.Any], **kwargs):
        for attr_name, attr_value in dct.items():
            if callable(attr_value):
                if not attr_name == "__init__":
                    continue
                dct[attr_name] = InjectedMeta.inject(attr_value)
        return super(InjectedMeta, cls).__new__(cls, name, bases, dct, **kwargs)

    @staticmethod
    def inject[**P, R](func: t.Callable[P, R]) -> t.Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            injected: dict[str, t.Any] = {}
            if (setting := Context.setting.get(None)) is not None:
                injected["setting"] = setting

            if (data := Context.data.get(None)) is not None:
                injected.update(data)

            injected.update(kwargs)
            return func(*args, **injected)

        return wrapper
