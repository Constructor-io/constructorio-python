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
        constructor = ConstructorIO(autocompleteKey=autocompleteKey)
        assert constructor._autocompleteKey == autocompleteKey

    def test_add():
        constructor = ConstructorIO(
            apiToken = "apiToken",
            autocompleteKey = "autocompleteKey",
            protocol = "http",
            host = "ac.cnstrc.com"
        )
        resp = constructor.add(
            item_name = "power drill",
            autocomplete_section = "standard"
        )
        # assert resp doesn't have error
        # assert response itself is blank

    def test_remove():
        constructor = ConstructorIO(
            apiToken = "apiToken",
            autocompleteKey = "autocompleteKey",
            protocol = "http",
            host = "ac.cnstrc.com"
        )
        resp = constructor.remove(
            item_name = "power drill",
            autocomplete_section = "standard"
        )
        # assert resp doesn't have error
        # assert response itself is blank

    def test_modify():
        constructor = ConstructorIO(
            apiToken = "apiToken",
            autocompleteKey = "autocompleteKey",
            protocol = "http",
            host = "ac.cnstrc.com"
        )
        resp = constructor.modify(
            item_name = "power drill",
            suggested_score = 100,
            autocomplete_section = "standard"
        )
        # assert resp doesn't have error
        # assert response itself is blank

    def test_conversion():
        constructor = ConstructorIO(
            apiToken = "apiToken",
            autocompleteKey = "autocompleteKey",
            protocol = "http",
            host = "ac.cnstrc.com"
        )
        resp = constructor.conversion(
            item_name = "power drill",
            autocomplete_section = "standard"
        )
        # assert resp doesn't have error
        # assert response itself is blank

    def test_search_no_num_res():
        constructor = ConstructorIO(
            apiToken = "apiToken",
            autocompleteKey = "autocompleteKey",
            protocol = "http",
            host = "ac.cnstrc.com"
        )
        resp = constructor.search(
            item_name = "power drill",
            autocomplete_section = "standard"
        )
        # assert resp doesn't have error
        # assert response itself is blank

    def test_search_num_res():
        constructor = ConstructorIO(
            apiToken = "apiToken",
            autocompleteKey = "autocompleteKey",
            protocol = "http",
            host = "ac.cnstrc.com"
        )
        resp = constructor.search(
            item_name = "power drill",
            num_results = 10,
            autocomplete_section = "standard"
        )
        # assert resp doesn't have error
        # assert response itself is blank

    def test_click_through():
        constructor = ConstructorIO(
            apiToken = "apiToken",
            autocompleteKey = "autocompleteKey",
            protocol = "http",
            host = "ac.cnstrc.com"
        )
        resp = constructor.click_through(
            item_name = "power drill",
            autocomplete_section = "standard"
        )
        # assert resp doesn't have error
        # assert response itself is blank
