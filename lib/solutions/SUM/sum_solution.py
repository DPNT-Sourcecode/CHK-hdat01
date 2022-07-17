# noinspection PyShadowingBuiltins,PyUnusedLocal

MIN_ALLOWED_VALUE = 0
MAX_ALLOWED_VALUE = 100


def _in_acceptable_range(value) -> bool:
    """
    Returns true if the given value is within acceptable range.
    """
    return value >= MIN_ALLOWED_VALUE and value <= MAX_ALLOWED_VALUE


def compute(x, y):

    # validate input params
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError("Only integers are allowed in compute function.")
    
    if not _in_acceptable_range(x):
        raise ValueError(f"param x must be between {MIN_ALLOWED_VALUE} and {MAX_ALLOWED_VALUE} inclusive.")
    
    if not _in_acceptable_range(y):
        raise ValueError(f"param y must be between {MIN_ALLOWED_VALUE} and {MAX_ALLOWED_VALUE} inclusive.")
    
    # return integer
    return x + y
