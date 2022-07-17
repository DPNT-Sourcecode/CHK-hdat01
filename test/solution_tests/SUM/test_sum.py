import pytest
from lib.solutions.SUM import MAX_ALLOWED_VALUE, MIN_ALLOWED_VALUE, sum_solution

class TestSum():
    def test_sum(self):
        assert sum_solution.compute(1, 2) == 3
    
    def test_x_is_not_integer_raises_typeerror(self):
        with pytest.raises(TypeError, match="Only integers are allowed in compute function."):
            sum_solution.compute(14.7, 1)
    
    def test_y_is_no_ingeger_raises_typeerror(self):
        with pytest.raises(TypeError, match="Only integers are allowed in compute function."):
            sum_solution.compute(1, 14.7)

    def test_x_is_less_than_min_allowed_value_raises_valueerror(self):
        with pytest.raises(TypeError, match=f"param x must be between {MIN_ALLOWED_VALUE} and {MAX_ALLOWED_VALUE} inclusive."):
            sum_solution.compute(-1, 14)

    def test_y_is_less_than_min_allowed_value_raises_valueerror(self):
        with pytest.raises(TypeError, match=f"param y must be between {MIN_ALLOWED_VALUE} and {MAX_ALLOWED_VALUE} inclusive."):
            sum_solution.compute(14, -1)


