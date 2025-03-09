from __future__ import annotations

import functools
import inspect
import typing as t


def inject[**P, R](func: t.Callable[P, R]) -> t.Callable[P, R]:
    """
    Injects AulosObject dependencies from the current Context into function arguments.

    This decorator automatically provides dependencies from the current Context
    for parameters that are subclasses of AulosObject.

    Args:
        func: The function to inject dependencies into

    Returns:
        Wrapped function with injected dependencies from Context
    """

    # get function signature
    sig = inspect.signature(func)

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        from aulos._core.object import AulosObject

        from .context import Context

        # get context data
        injectables = Context.injectables.get({})

        for param_name in sig.parameters:
            if (
                param_name not in kwargs
                and param_name in injectables
                and isinstance(injectables[param_name], AulosObject)
            ):
                kwargs[param_name] = injectables[param_name]

        return func(*args, **kwargs)

    return wrapper
