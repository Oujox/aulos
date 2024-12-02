import typing as t
from functools import wraps


def inject[**P, R](func: t.Callable[P, R]) -> t.Callable[P, R]:
    """設定ファイルを依存注入
    * __init__, classmethod での使用を想定
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        from ...utils import Context

        if "setting" not in kwargs.keys():
            setting = Context.internal.get(None)
            return func(*args, setting=setting, **kwargs)
        return func(*args, **kwargs)

    return wrapper
