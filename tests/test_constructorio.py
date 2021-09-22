from constructorio_python.constructorio import ConstructorIO

class TestConstructorIO():
    def test_nothing(self):
        client = ConstructorIO()
        assert client is not None
