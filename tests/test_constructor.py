import pytest
from constructorio import ConstructorIO

class something:
    def test_encodes_parameters():
        constructor = ConstructorIO()
        serialized_params = constructor\
            ._serializeParams({foo: [1, 2], bar: {baz: ['a', 'b']}})
        assert serialized_params == 'foo%5B%5D=1&foo%5B%5D=2&bar%5Bbaz%5D%5B%5D=a&bar%5Bbaz%5D%5B%5D=b'

    def test_creates_urls_correctly():
        constructor = ConstructorIO(autocompleteKey="a-test-autocomplete-key")
        generated_url = constructor._makeUrl('test')
        assert generated_url == 'https://ac.cnstrc.com/v1/test?autocomplete_key=a-test-autocomplete-key'

    def test_set_api_token():
        apiToken = 'a-test-api-key',
        constructor = ConstructorIO(apiToken=apiToken)
        assert constructor._apiToken == apiToken

    def test_set_ac_key():
        autocompleteKey = 'a-test-autocomplete-key'
        constructor = CosntructorIO(autocompleteKey=autocompleteKey)
        assert constructor._autocompleteKey == autocompleteKey

    def test_add():
        pass

    def test_remove():
        pass

    def test_modify():
        pass

    def test_conversion():
        pass

    def test_search():
        pass

    def test_click_through():
        pass
