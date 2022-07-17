from lib.solutions.CHK.checkout_solution import checkout, INVALID_SKUS_RETURN_VALUE

class TestCHK():
    def test_checkout_with_invalid_type_returns_expected_value(self):
        assert checkout(12345) == INVALID_SKUS_RETURN_VALUE

    def test_checkout_with_empty_string_returns_expected_value(self):
        assert checkout("") == INVALID_SKUS_RETURN_VALUE

    def test_checkout_with_invalid_product_returns_expected_value(self):
        assert checkout("A,B,D,F") == INVALID_SKUS_RETURN_VALUE


