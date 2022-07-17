from lib.solutions.SUM import sum_solution


class TestSum():
    def test_sum(self):
        assert sum_solution.compute(1, 2) == 3
    
    def test_x_is_not_integer_raises_typeerror(self):
        pass
    
    def test_y_is_no_ingeger_raises_typeerror(self):
        pass

    def test_x_is_less_than_min_allowed_value_raises_valueerror(self):
        pass

    def test_y_is_less_than_min_allowed_value_raises_valueerror(self):
        pass

