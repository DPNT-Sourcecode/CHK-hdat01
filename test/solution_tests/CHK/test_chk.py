from lib.solutions.CHK.checkout_solution import checkout, EMPTY_SKUS_RETURN_VALUE, INVALID_SKUS_RETURN_VALUE

class TestCHK():
    def test_checkout_with_invalid_type_returns_expected_value(self):
        assert checkout(12345) == INVALID_SKUS_RETURN_VALUE

    def test_checkout_with_empty_string_returns_expected_value(self):
        assert checkout("") == EMPTY_SKUS_RETURN_VALUE

    def test_checkout_with_invalid_product_returns_expected_value(self):
        assert checkout("A,B,D,F") == INVALID_SKUS_RETURN_VALUE

    def test_checkout_with_no_offers_applied_returns_expected_amount(self):
        assert checkout("A,B,C,D") == 115
    
    def test_product_a_offer_applied_correctly(self):
        assert checkout("AAAAABCD") == 265
    
    def test_procut_b_offer_applied_correctly(self):
        assert checkout("AAAABBBCD") == 290
    
    def test_lower_case_string_returns_as_invalid_value(self):
        assert checkout("a") == INVALID_SKUS_RETURN_VALUE
    
    def test_multiple_offers_applied_in_customer_preference(self):
        assert checkout("AAAAAAAA") == 330

    def test_multiple_offers_applied_in_customer_preference(self):
        assert checkout("AAAAAAAAA") == 380


