import typing as t
from functools import wraps

from .coexistence import Coexistence
from .context import Context


def coexist[**P, R](func: t.Callable[P, R]) -> t.Callable[P, R]:
    """オブジェクトの共存性チェックを有効化
    * インスタンスメソッドでの使用を想定
    """

    @wraps(func)
    def wrapper(instance: Coexistence, *args: P.args, **kwargs: P.kwargs) -> R:
        if (coexist := Context.coexist.get(None)) is not None:
            if coexist and isinstance(instance, Coexistence):
                for arg in args:
                    if isinstance(arg, Coexistence):
                        if not instance.can_coexist(arg):
                            print(instance._i_coexistence, arg._t_coexistence)
                            raise Exception()
                for _, kwarg in kwargs.items():
                    if isinstance(kwarg, Coexistence):
                        if not instance.can_coexist(kwarg):
                            raise Exception()
        return func(instance, *args, **kwargs)

    return wrapper
