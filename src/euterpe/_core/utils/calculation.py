import typing as t


def wrapped_diff(lhs: int, rhs: int, max: t.Optional[int] = None) -> int:
    if max is not None:
        result1 = lhs - rhs
        result2 = (lhs + (max if lhs < rhs else 0)) - (rhs + (max if lhs > rhs else 0))
        return result1 if abs(result1) < abs(result2) else result2
    return lhs - rhs
