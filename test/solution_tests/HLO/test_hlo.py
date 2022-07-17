from lib.solutions.HLO.hello_solution import hello

class TestSum():
    def test_hello_returns_expected_string_with_no_name_provided(self):
        assert hello("") == "Hello World"