from enum import Enum
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
    GROUP_BUY = "GROUP_BUY"


class Offer:

    def __init__(self, offer_type, threshold, amount = None, target_products = []):
        self.offer_type = offer_type
        self.threshold = threshold
        self.amount = amount
        self.target_products = target_products

        self._product_sku = None
    
    @property
    def is_multibuy(self) -> bool:
        return self.offer_type == OfferType.MULTI_BUY
    
    @property
    def is_free_product(self) -> bool:
        return self.offer_type == OfferType.FREE_PRODUCT

    def set_product(self, product_sku):
        if product_sku in self.target_products and self.is_free_product:
            self.threshold += 1
        self._product_sku = product_sku


class Product:

    def __init__(self, sku, price, offers = []):
        self.sku = sku
        self.price = price
        for offer in offers:
            offer.set_product(self.sku)
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

    def __init__(self, product_data: dict, group_buy_offers = []):
        products = []
        for sku, data in product_data.items():
            products.append(
                Product(sku, data.get("price"), offers=data.get("offers"))
            )

        self.products = {product.sku: product for product in products}
        self.group_buy_offers = group_buy_offers

    
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

    DEFAULT_GROUP_BUY_TARGETS = [
        PRODUCT_S,
        PRODUCT_T,
        PRODUCT_X,
        PRODUCT_Y,
        PRODUCT_Z,
    ]

    group_buy_offer = Offer(offer_type=OfferType.GROUP_BUY, threshold=3, amount=45, target_products=DEFAULT_GROUP_BUY_TARGETS)


    DATA_TO_IMPORT = {
        "A": {"price": 50, "offers": [Offer(offer_type=OfferType.MULTI_BUY, threshold=3, amount=130),Offer(offer_type=OfferType.MULTI_BUY, threshold=5, amount=200),]},
        "B": {"price": 30, "offers": [Offer(offer_type=OfferType.MULTI_BUY, threshold=2, amount=45)]},
        "C": {"price": 20, "offers": []},
        "D": {"price": 15, "offers": []},
        "E": {"price": 40, "offers": [Offer(offer_type=OfferType.FREE_PRODUCT, threshold=2, target_products=[PRODUCT_B])]},
        "F": {"price": 10, "offers": [Offer(offer_type=OfferType.FREE_PRODUCT, threshold=2, target_products=[PRODUCT_F])]},
        "G": {"price": 20, "offers": []},
        "H": {"price": 10, "offers": [Offer(offer_type=OfferType.MULTI_BUY, threshold=5, amount=45),Offer(offer_type=OfferType.MULTI_BUY, threshold=10, amount=80)]},
        "I": {"price": 35, "offers": []},
        "J": {"price": 60, "offers": []},
        "K": {"price": 70, "offers": [Offer(offer_type=OfferType.MULTI_BUY, threshold=2, amount=150)]},
        "L": {"price": 90, "offers": []},
        "M": {"price": 15, "offers": []},
        "N": {"price": 40, "offers": [Offer(offer_type=OfferType.FREE_PRODUCT, threshold=3, target_products=[PRODUCT_M])]},
        "O": {"price": 10, "offers": []},
        "P": {"price": 50, "offers": [Offer(offer_type=OfferType.MULTI_BUY, threshold=5, amount=200)]},
        "Q": {"price": 30, "offers": [Offer(offer_type=OfferType.MULTI_BUY, threshold=3, amount=80)]},
        "R": {"price": 50, "offers": [Offer(offer_type=OfferType.FREE_PRODUCT, threshold=3, target_products=[PRODUCT_Q])]},
        "S": {"price": 20, "offers": []},
        "T": {"price": 20, "offers": []},
        "U": {"price": 40, "offers": [Offer(offer_type=OfferType.FREE_PRODUCT, threshold=3, target_products=[PRODUCT_U])]},
        "V": {"price": 50, "offers": [Offer(offer_type=OfferType.MULTI_BUY, threshold=2, amount=90),Offer(offer_type=OfferType.MULTI_BUY, threshold=3, amount=130)]},
        "W": {"price": 20, "offers": []},
        "X": {"price": 17, "offers": []},
        "Y": {"price": 20, "offers": []},
        "Z": {"price": 21, "offers": []},
    }

    # set up products
    products_store = ProductsStore(DATA_TO_IMPORT, group_buy_offers=[group_buy_offer])
    
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
    skus_free_products_applied = split_skus
    for offer in products_store.get_all_free_product_offers():
        
        product_count = skus_free_products_applied.count(offer._product_sku)

        if not product_count:
            continue
        
        num_to_remove, remainder = divmod(product_count, offer.threshold)

        if num_to_remove == 0:
            continue
        
        removed = 0
        filtered_skus = []
        for sku in skus_free_products_applied:
            if sku not in offer.target_products:
                filtered_skus.append(sku)
            elif removed != num_to_remove:
                removed += 1
                continue
            else:
                filtered_skus.append(sku)

        skus_free_products_applied = filtered_skus
    
    amount = 0
    
    final_skus = skus_free_products_applied
    # secondly apply group buy offers
    for offer in products_store.group_buy_offers:
        product_group = offer.target_products
        
        # need to prioritise the highest value product
        ordered_products = sorted([products_store.products.get(sku) for sku in product_group], key=lambda p: p.price, reverse=True)
        
        
        sku_counts = {sku: final_skus.count(sku) for sku in product_group}
        
        if len([key for key in sku_counts if sku_counts[key] > 0]) < offer.threshold:
            continue
        
        sku_count_filtered = {key: value for key, value in sku_counts.items() if value > 0}
        lowest_common_occurences = min(sku_count_filtered, key=sku_count_filtered.get)

        # ----- fix
        filtered_skus = []
        for i in range(0, sku_count_filtered.get(lowest_common_occurences)):
            for product in ordered_products:

                for sku in final_skus:
                    if sku not in product_group:
                        filtered_skus.append(sku)
        final_skus = filtered_skus

    print(final_skus)
    # lastly apply multibuy offers
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
    

