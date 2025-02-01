def cyclic_difference(lhs: int, rhs: int, cycle_length: int | None = None) -> int:
    if cycle_length is not None:
        result1 = lhs - rhs
        result2 = (lhs + (cycle_length if lhs < rhs else 0)) - (rhs + (cycle_length if lhs > rhs else 0))
        return result1 if abs(result1) < abs(result2) else result2
    return lhs - rhs
