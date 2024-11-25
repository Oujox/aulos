import typing as t


def diff(lhs: int, rhs: int, max: t.Optional[int] = None) -> int:
    """特殊な差分計算"""
    if isinstance(max, int):
        result1 = lhs - rhs
        result2 = (lhs + (max if lhs < rhs else 0)) - (rhs + (max if lhs > rhs else 0))
        return result1 if abs(result1) < abs(result2) else result2
    return lhs - rhs
