INVALID_SKUS_RETURN_VALUE = -1
ACCEPTED_DELIMITERS = [",", "|"]

PRODUCT_A = "A"
PRODUCT_B = "B"
PRODUCT_C = "C"
PRODUCT_D = "D"

PRICING = {
    PRODUCT_A: {"price": 50, "offer_threshold": 3, "offer_amount": 130},
    PRODUCT_B: {"price": 30, "offer_threshold": 2, "offer_amount": 45},
    PRODUCT_C: {"price": 20, "offer_threshold": None, "offer_amount": None},
    PRODUCT_D: {"price": 15, "offer_threshold": None, "offer_amount": None},
}

PRODUCT_A_OFFER_THRESHOLD = 3
PRODUCT_A_OFFER_AMOUNT = 130
PRODUCT_B_OFFER_THRESHOLD = 2
PRODUCT_B_OFFER_AMOUNT = 45

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
    # also remove all whitespace
    skus = skus.upper().strip().replace(" ", "")
    
    # find first delimiter, then split on that
    found_delimiter = _find_delimiter(skus)
    split_skus = skus.split(found_delimiter) if found_delimiter else list(skus)
    
    # treat any invalid products as an invalid string - may need to change later
    contains_invalid_product = any([sku for sku in split_skus if sku not in PRICING.keys()])

    if contains_invalid_product:
        return INVALID_SKUS_RETURN_VALUE

    # product_a_count = split_skus.count(PRODUCT_A)
    # if product_a_count >= PRODUCT_A_OFFER_THRESHOLD:


    return sum([PRICING.get(sku) for sku in split_skus])
    





