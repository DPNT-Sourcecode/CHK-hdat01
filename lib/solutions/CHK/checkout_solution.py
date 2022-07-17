from concurrent.futures import process
from enum import Enum
from posixpath import split
from typing import List


INVALID_SKUS_RETURN_VALUE = -1
EMPTY_SKUS_RETURN_VALUE = 0
ACCEPTED_DELIMITERS = [",", "|"]

PRODUCT_A = "A"
PRODUCT_B = "B"
PRODUCT_C = "C"
PRODUCT_D = "D"
PRODUCT_E = "E"


class OfferType(Enum):
    MULTI_BUY = "MULTI_BUY"
    FREE_PRODUCT = "FREE_PRODUCT"




class Offer:

    def __init__(self, offer_type, threshold, amount = None, target_product = None):
        self.offer_type = offer_type
        self.threshold = threshold
        self.amount = amount
        self.target_product = target_product
    
    @property
    def is_multibuy(self) -> bool:
        return self.offer_type == OfferType.MULTI_BUY
    
    @property
    def is_free_product(self) -> bool:
        return self.offer_type == OfferType.FREE_PRODUCT


class Product:

    def __init__(self, sku, price, offers = []):
        self.sku = sku
        self.price = price
        self.offers = offers
    
    def get_offers(self) -> List[Offer]:
        """
        Get offers ordered by the max discount
        """
        return sorted(self.offers, key=lambda t: t.amount, reverse=True)


def _find_delimiter(skus):
    # TODO: refactor
    found_delimiter = None
    for delimiter in ACCEPTED_DELIMITERS:
        if delimiter in skus:
            found_delimiter = delimiter
            break
    return found_delimiter


class ProductsStore:

    def __init__(self):
        product_a_offers = [
            Offer(offer_type=OfferType.MULTI_BUY, threshold=3, amount=130),
            Offer(offer_type=OfferType.MULTI_BUY, threshold=5, amount=200),
        ]
        product_b_offers = [
            Offer(offer_type=OfferType.MULTI_BUY, threshold=2, amount=45),
        ]
        product_e_offers = [
            Offer(offer_type=OfferType.FREE_PRODUCT, threshold=2, target_product=PRODUCT_B),
        ]
        product_a = Product(sku=PRODUCT_A, price=50, offers=product_a_offers)
        product_b = Product(sku=PRODUCT_B, price=30, offers=product_b_offers)
        product_c = Product(sku=PRODUCT_C, price=20)
        product_d = Product(sku=PRODUCT_D, price=15)
        product_e = Product(sku=PRODUCT_E, price=40, offers=product_e_offers)

        products = [
            product_a,
            product_b,
            product_c,
            product_d,
            product_e,
        ]
        self.products = {product.sku: product for product in products}

    
    def get_all_product_skus(self) -> List[str]:
        return self.products.keys()



# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):

    # set up products
    products_store = ProductsStore()
    
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
    contains_invalid_product = any([sku for sku in split_skus if sku not in products_store.get_all_product_skus()])

    if contains_invalid_product:
        return INVALID_SKUS_RETURN_VALUE


    # NOTE: this works for small product lists, but if there were 10000000s of products this would need to change
    # could maybe look up the data we need first, then perform calculations
    amount = 0
    for product_sku, product in products_store.products.items():

        # move onto next product if not present
        if product_sku not in split_skus:
            continue
        
        offers = product.get_offers()
        
        product_count = split_skus.count(product_sku)

        offers = product.get_offers()
        if not offers:
            amount += product_count * product.price
        
        offers_expended = False
        remaining_product_count = 0
        for offer in offers:
            if offers_expended:
                break
            current_count = remaining_product_count if remaining_product_count > 0 else product_count
            match_count, remainder = divmod(current_count, offer.threshold)
            amount += match_count * offer.amount
            remaining_product_count = remainder
            offers_expended = remainder == 0

        amount += remaining_product_count * product.price





        # if not offers or not any([product_count < offer.threshold for offer in product.get_offers()]):
        #     amount += product_count * product.price

        # if no offers just add as normal (TODO: handle when 2E => free B)
        # if not offers:
        #     amount += product_count * product.price
        #     continue

        
        # for offer in product.get_offers():
        #     if offer.offer_type == OfferType.MULTI_BUY:
            
        #         # get product data
        #         offer_threshold = offer.threshold
        #         product_price = product.price
                
        #         # get number of times offer is applicable, if never over threshold, just add normally
        #         matching_offer_count = product_count // offer_threshold
        #         if matching_offer_count == 0:
        #             amount += product_count * product_price
        #             continue

        #         # calculate total matching offers and add remaining amounts normally
        #         offer_amount = offer.amount
        #         total_offer_amount = matching_offer_count * offer_amount
        #         remaining_amount = (product_count % offer_threshold) * product_price
        #         amount += (total_offer_amount + remaining_amount)

    return amount
    




