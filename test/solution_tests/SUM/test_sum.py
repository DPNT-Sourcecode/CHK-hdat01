import pytest
from lib.solutions.SUM.sum_solution import compute, MAX_ALLOWED_VALUE, MIN_ALLOWED_VALUE

class TestSum():
    def test_sum(self):
        assert compute(1, 2) == 3
    
    def test_x_is_not_integer_raises_typeerror(self):
        raised = False
        try:
            compute(14.7, 1)
        except TypeError:
            raised = True
        assert raised is True
    
    def test_y_is_no_ingeger_raises_typeerror(self):
        raised = False
        try:
            compute(14, 1.4)
        except TypeError:
            raised = True
        assert raised is True

    def test_x_is_less_than_min_allowed_value_raises_valueerror(self):
        raised = False
        try:
            compute(-1, 14)
        except ValueError:
            raised = True
        assert raised is True

    def test_y_is_less_than_min_allowed_value_raises_valueerror(self):
        raised = False
        try:
            compute(1, -14)
        except ValueError:
            raised = True
        assert raised is True

    def test_x_is_greater_than_max_allowed_value_raises_valueerror(self):
        raised = False
        try:
            compute(150, 14)
        except ValueError:
            raised = True
        assert raised is True

    def test_y_is_greater_than_max_allowed_value_raises_valueerror(self):
        raised = False
        try:
            compute(1, 150)
        except ValueError:
            raised = True
        assert raised is True
