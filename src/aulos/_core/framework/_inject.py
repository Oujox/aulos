import typing as t
from functools import wraps


def inject[**P, R](func: t.Callable[P, R]) -> t.Callable[P, R]:
    """依存注入
    * __init__, classmethod での使用を想定
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        from .context import Context

        if (injected := Context.internal.get(None)) is not None:
            injected.update(kwargs)
            return func(*args, **injected)
        return func(*args, **kwargs)

    return wrapper
