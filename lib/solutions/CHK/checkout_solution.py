INVALID_SKUS_RETURN_VALUE = -1
ACCEPTED_DELIMITERS = [",", "|"]

PRICING = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
}

def _find_delimiter(skus):
    # TODO: refactor
    found_delimiter = None
    for delimiter in ACCEPTED_DELIMITERS:
        if delimiter in skus:
            found_delimiter = delimiter
            break
    return found_delimiter

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    
    # we don't currently know how SKUs will be split, or if there will be a delimiter at all
    
    # I think all python3 strings are unicode by default

    if not isinstance(skus, str):
        return INVALID_SKUS_RETURN_VALUE
    
    if len(skus) == 0:
        return INVALID_SKUS_RETURN_VALUE
    
    # convert to all uppercase - this may need to change if we want to ignore lowercase chars
    skus = skus.upper()
    
    # find first delimiter, then split on that
    found_delimiter = _find_delimiter(skus)
    split_skus = skus.split(found_delimiter) if found_delimiter else list(skus)
    split_skus = 




