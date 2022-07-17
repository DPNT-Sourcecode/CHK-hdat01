from concurrent.futures import process
from enum import Enum
from posixpath import split
from re import L
from typing import List


INVALID_SKUS_RETURN_VALUE = -1
EMPTY_SKUS_RETURN_VALUE = 0
ACCEPTED_DELIMITERS = [",", "|"]

PRODUCT_A = "A"
PRODUCT_B = "B"
PRODUCT_C = "C"
PRODUCT_D = "D"
PRODUCT_E = "E"
PRODUCT_F = "F"
PRODUCT_G = "G"
PRODUCT_H = "H"
PRODUCT_I = "I"
PRODUCT_J = "J"
PRODUCT_K = "K"
PRODUCT_L = "L"
PRODUCT_M = "M"
PRODUCT_N = "N"
PRODUCT_O = "O"
PRODUCT_P = "P"
PRODUCT_Q = "Q"
PRODUCT_R = "R"
PRODUCT_S = "S"
PRODUCT_T = "T"
PRODUCT_U = "U"
PRODUCT_V = "V"
PRODUCT_W = "W"
PRODUCT_X = "X"
PRODUCT_Y = "Y"
PRODUCT_Z = "Z"


class OfferType(Enum):
    MULTI_BUY = "MULTI_BUY"
    FREE_PRODUCT = "FREE_PRODUCT"


class Offer:

    def __init__(self, offer_type, threshold, amount = None, target_product = None):
        self.offer_type = offer_type
        self.threshold = threshold
        self.amount = amount
        self.target_product = target_product

        self._product = None
    
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
        for offer in offers:
            if not offer.is_free_product:
                continue
            offer._product = self
            if offer.target_product == self.sku:
                offer.threshold += 1
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


DATA_TO_IMPORT = {
    "A": {
        "price": 50,
        "offers": [
            Offer(offer_type=OfferType.MULTI_BUY, threshold=3, amount=130),
            Offer(offer_type=OfferType.MULTI_BUY, threshold=5, amount=200),
        ]
    },
    "B": {"price": 30, "offers": [Offer(offer_type=OfferType.MULTI_BUY, threshold=2, amount=45)]},
    "C": {"price": 20, "offers": []},
    "D": {"price": 15, "offers": []},
    "E": {"price": 40, "offers": [Offer(offer_type=OfferType.FREE_PRODUCT, threshold=2, target_product=PRODUCT_B)]},
    "F": {"price": 10, "offers": [Offer(offer_type=OfferType.FREE_PRODUCT, threshold=2, target_product=PRODUCT_F)]},
    "G": {"price": 20, "offers": []},
    "H": {"price": 10, "offers": [
            Offer(offer_type=OfferType.MULTI_BUY, threshold=5, amount=45),
            Offer(offer_type=OfferType.MULTI_BUY, threshold=10, amount=80),
        ]
    },
    "I": {"price": 35, "offers": []},
    "J": {"price": 60, "offers": []},
    "K": {"price": 80, "offers": [Offer(offer_type=OfferType.MULTI_BUY, threshold=2, amount=150)]},
    "L": {"price": 90, "offers": []},
    "M": {"price": 15, "offers": []},
    "N": {"price": 40, "offers": [Offer(offer_type=OfferType.FREE_PRODUCT, threshold=3, target_product=PRODUCT_M)]},
    "O": {"price": 10, "offers": []},
    "P": {"price": 50, "offers": [Offer(offer_type=OfferType.MULTI_BUY, threshold=5, amount=200)]},
    "Q": {"price": 30, "offers": [Offer(offer_type=OfferType.MULTI_BUY, threshold=3, amount=80)]},
    "R": {"price": 50, "offers": [Offer(offer_type=OfferType.FREE_PRODUCT, threshold=3, target_product=PRODUCT_Q)]},
    "S": {"price": 30, "offers": []},
    "T": {"price": 20, "offers": []},
    "U": {"price": 40, "offers": [Offer(offer_type=OfferType.FREE_PRODUCT, threshold=3, target_product=PRODUCT_U)]},
    "V": {"price": 50, "offers": [
            Offer(offer_type=OfferType.MULTI_BUY, threshold=2, amount=90),
            Offer(offer_type=OfferType.MULTI_BUY, threshold=3, amount=130),
        ]
    },
    "W": {"price": 20, "offers": []},
    "X": {"price": 90, "offers": []},
    "Y": {"price": 10, "offers": []},
    "Z": {"price": 50, "offers": []},
}


class ProductsStore:

    def __init__(self, product_data: dict):
        # product_a_offers = [
        #     Offer(offer_type=OfferType.MULTI_BUY, threshold=3, amount=130),
        #     Offer(offer_type=OfferType.MULTI_BUY, threshold=5, amount=200),
        # ]
        # product_b_offers = [
        #     Offer(offer_type=OfferType.MULTI_BUY, threshold=2, amount=45),
        # ]
        # product_e_offers = [
        #     Offer(offer_type=OfferType.FREE_PRODUCT, threshold=2, target_product=PRODUCT_B),
        # ]
        # product_f_offers = [
        #     Offer(offer_type=OfferType.FREE_PRODUCT, threshold=2, target_product=PRODUCT_F),
        # ]
        # product_a = Product(sku=PRODUCT_A, price=50, offers=product_a_offers)
        # product_b = Product(sku=PRODUCT_B, price=30, offers=product_b_offers)
        # product_c = Product(sku=PRODUCT_C, price=20)
        # product_d = Product(sku=PRODUCT_D, price=15)
        # product_e = Product(sku=PRODUCT_E, price=40, offers=product_e_offers)
        # product_f = Product(sku=PRODUCT_F, price=10, offers=product_f_offers)

        products = []
        for sku, data in product_data.items():
            products.append(
                Product(sku, data.get("price"), offers=data.get("offers"))
            )

        self.products = {product.sku: product for product in products}

    
    def get_all_product_skus(self) -> List[str]:
        return self.products.keys()
    
    def get_all_free_product_offers(self) -> List[Offer]:
        offers = []
        for product in self.products.values():
            for offer in product.get_offers():
                if offer.is_free_product:
                    offers.append(offer)
        return offers

    def get_all_multibuy_offers(self) -> List[Offer]:
        offers = []
        for product in self.products.values():
            for offer in product.get_offers():
                if offer.is_multibuy:
                    offers.append(offer)
        return offers


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):

    # set up products
    products_store = ProductsStore(DATA_TO_IMPORT)
    
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

    # firstly apply any free product offers
    final_skus = split_skus
    for offer in products_store.get_all_free_product_offers():
        print(offer._product.sku)
        
        product_count = final_skus.count(offer._product.sku)

        if not product_count:
            continue
        
        num_to_remove, remainder = divmod(product_count, offer.threshold)
        print(offer._product.sku, offer.target_product,offer.threshold, num_to_remove, product_count)

        if num_to_remove == 0:
            continue
        
        removed = 0
        filtered_skus = []
        for sku in final_skus:
            if sku != offer.target_product:
                filtered_skus.append(sku)
            elif removed != num_to_remove:
                removed += 1
                continue
            else:
                filtered_skus.append(sku)

        final_skus = filtered_skus

    print(final_skus)
    amount = 0
    for product_sku, product in products_store.products.items():

        # move onto next product if not present
        product_count = final_skus.count(product_sku)
        if not product_count:
            continue

        offers = [offer for offer in product.get_offers() if offer.is_multibuy]
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


    return amount
    
