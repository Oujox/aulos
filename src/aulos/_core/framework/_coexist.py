import typing as t
from functools import wraps


def coexist[**P, R](func: t.Callable[P, R]) -> t.Callable[P, R]:
    """オブジェクトの共存性チェックを有効化
    * インスタンスメソッドでの使用を想定
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        from ...utils import Context

        if "setting" not in kwargs.keys():
            setting = Context.setting()
            return func(*args, setting=setting, **kwargs)
        return func(*args, **kwargs)

    return wrapper
