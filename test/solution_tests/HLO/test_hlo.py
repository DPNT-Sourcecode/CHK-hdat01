from lib.solutions.HLO.hello_solution import hello

class TestSum():
    def test_hello_returns_expected_string_with_name(self):
        assert hello("test") == "Hello, test!"
    
    def test_invalid_name_type_raises_typeerror(self):
        raised = False
        try:
            hello(123545)
        except TypeError:
            raised = True
        assert raised is True