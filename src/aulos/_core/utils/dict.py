import typing as t


def convert_lists_to_tuples(obj: dict[str, t.Any]) -> dict[str, t.Any]:
    """
    Recursively converts lists in a dictionary or list to tuples.

    Args:
        obj (Any): The input object to process (dict, list, or other types).

    Returns:
        Any: The processed object with lists converted to tuples.
    """
    if isinstance(obj, dict):
        return {key: convert_lists_to_tuples(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return tuple(convert_lists_to_tuples(element) for element in obj)
    else:
        return obj
