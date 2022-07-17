INVALID_SKUS_RETURN_VALUE = -1
ACCEPTED_DELIMITERS = [",", "|"]

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    
    # we don't currently know how SKUs will be split, or if there will be a delimiter at all
    
    # I think all python3 strings are unicode by default

    if not isinstance(skus, str):
        return INVALID_SKUS_RETURN_VALUE
    
    # attempt to split on delimiters: find first delimiter, then split on that
    found_delimiter = None
    for delimiter in ACCEPTED_DELIMITERS:
        if delimiter in skus:
            found_delimiter = delimiter
            break

    if found_delimiter:
        split_skus = skus.split(delimiter)


