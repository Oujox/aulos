import typing as t
from functools import wraps

from .context import Context


def inject[**P, R](func: t.Callable[P, R]) -> t.Callable[P, R]:
    """依存注入
    * __init__, classmethod での使用を想定
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        injected = {}
        if (setting := Context.setting.get(None)) is not None:
            injected["setting"] = setting

        if (data := Context.data.get(None)) is not None:
            injected.update(data)

        injected.update(kwargs)
        return func(*args, **injected)

    return wrapper
