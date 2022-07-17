# noinspection PyShadowingBuiltins,PyUnusedLocal

MIN_ALLOWED_VALUE = 0
MAX_ALLOWED_VALUE = 100


def _in_acceptable_range(value) -> bool:
    """
    Returns true if the given value is within acceptable range.
    """
    return value >= MIN_ALLOWED_VALUE and value <= MAX_ALLOWED_VALUE


def compute(x, y):

    if not isinstance(x, int) or not isinstance(y, int):
        raise ValueError("Only integers are allowed in compute function.")
    
    raise NotImplementedError()

