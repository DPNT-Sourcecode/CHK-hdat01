from posixpath import split


INVALID_SKUS_RETURN_VALUE = -1
EMPTY_SKUS_RETURN_VALUE = 0
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
    
    # treat empty sku string as non-invalid
    if len(skus) == 0:
        return EMPTY_SKUS_RETURN_VALUE
    
    # convert to all uppercase - this may need to change if we want to ignore lowercase chars
    # also remove all whitespace
    skus = skus.strip().replace(" ", "")
    
    # find first delimiter, then split on that
    found_delimiter = _find_delimiter(skus)
    split_skus = skus.split(found_delimiter) if found_delimiter else list(skus)
    
    # treat any invalid products as an invalid string - may need to change later
    contains_invalid_product = any([sku for sku in split_skus if sku not in PRICING.keys()])

    if contains_invalid_product:
        return INVALID_SKUS_RETURN_VALUE


    # NOTE: this works for small product lists, but if there were 10000000s of products this would need to change
    # could maybe look up the data we need first, then perform calculations
    amount = 0
    for product, product_data in PRICING.items():

        # move onto next product if not present
        if product not in split_skus:
            continue
        
        # get product data
        offer_threshold = product_data.get("offer_threshold")
        product_count = split_skus.count(product)
        product_price = product_data.get("price")
        
        # if no offer, just add normally
        if not offer_threshold:
            amount += product_count * product_price
            continue
        
        # get number of times offer is applicable, if never over threshold, just add normally
        matching_offer_count = product_count // offer_threshold
        if matching_offer_count == 0:
            amount += product_count * product_price
            continue
        
        # calculate total matching offers and add remaining amounts normally
        offer_amount = product_data.get("offer_amount")
        total_offer_amount = matching_offer_count * offer_amount
        remaining_amount = (product_count % offer_threshold) * product_price
        amount += (total_offer_amount + remaining_amount)

    return amount
    
