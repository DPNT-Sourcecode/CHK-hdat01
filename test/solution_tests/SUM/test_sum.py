import pytest
from lib.solutions.SUM.sum_solution import compute, MAX_ALLOWED_VALUE, MIN_ALLOWED_VALUE

class TestSum():
    def test_sum(self):
        assert compute(1, 2) == 3
    
    def test_x_is_not_integer_raises_typeerror(self):
        with pytest.raises(TypeError, match="Only integers are allowed in compute function."):
            compute(14.7, 1)
    
    def test_y_is_no_ingeger_raises_typeerror(self):
        with pytest.raises(TypeError, match="Only integers are allowed in compute function."):
            compute(1, 14.7)

    def test_x_is_less_than_min_allowed_value_raises_valueerror(self):
        with pytest.raises(TypeError, match=f"param x must be between {MIN_ALLOWED_VALUE} and {MAX_ALLOWED_VALUE} inclusive."):
            compute(-1, 14)

    def test_y_is_less_than_min_allowed_value_raises_valueerror(self):
        with pytest.raises(TypeError, match=f"param y must be between {MIN_ALLOWED_VALUE} and {MAX_ALLOWED_VALUE} inclusive."):
            compute(14, -1)



