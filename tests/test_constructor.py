import pytest
from constructorio import ConstructorIO

class TestConstructorIO:

    def test_encodes_parameters(self):
        constructor = ConstructorIO()
        serialized_params = constructor\
            ._serializeParams({'foo': [1, 2], 'bar': {'baz': ['a', 'b']}})
        assert serialized_params == "foo=%5B1%2C+2%5D&bar=%7B%27baz%27%3A+%5B%27a%27%2C+%27b%27%5D%7D"

    def test_creates_urls_correctly(self):
        constructor = ConstructorIO(autocompleteKey="a-test-autocomplete-key")
        generated_url = constructor._makeUrl('v1/test')
        assert generated_url == 'https://ac.cnstrc.com/v1/test?autocomplete_key=a-test-autocomplete-key'

    def test_set_api_token(self):
        apiToken = 'a-test-api-key',
        constructor = ConstructorIO(apiToken=apiToken)
        assert constructor._apiToken == apiToken

    def test_set_ac_key(self):
        autocompleteKey = 'a-test-autocomplete-key'
        constructor = ConstructorIO(autocompleteKey=autocompleteKey)
        assert constructor._autocompleteKey == autocompleteKey

    def test_ac_query(self):
        constructor = ConstructorIO(
            apiToken = "apiToken",
            autocompleteKey = "autocompleteKey",
            protocol = "http",
            host = "ac.cnstrc.com"
        )
        resp = constructor.query(
            queryStr = "a"
        )
        assert resp.status_code == 200
        assert resp.text != ""

    def test_add(self):
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
        assert resp.status_code == 204
        assert resp.text == ""

    def test_remove(self):
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
        assert resp.status_code == 204
        assert resp.text == ""

    def test_modify(self):
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
        assert resp.status_code == 204
        assert resp.text == ""

    def test_conversion(self):
        constructor = ConstructorIO(
            apiToken = "apiToken",
            autocompleteKey = "autocompleteKey",
            protocol = "http",
            host = "ac.cnstrc.com"
        )
        resp = constructor.track_conversion(
            term = "power drill",
            autocomplete_section = "standard"
        )
        assert resp.status_code == 204
        assert resp.text == ""

    def test_search_no_num_res(self):
        constructor = ConstructorIO(
            apiToken = "apiToken",
            autocompleteKey = "autocompleteKey",
            protocol = "http",
            host = "ac.cnstrc.com"
        )
        resp = constructor.track_search(
            term = "power drill",
            autocomplete_section = "standard"
        )
        assert resp.status_code == 204
        assert resp.text == ""

    def test_search_num_res(self):
        constructor = ConstructorIO(
            apiToken = "apiToken",
            autocompleteKey = "autocompleteKey",
            protocol = "http",
            host = "ac.cnstrc.com"
        )
        resp = constructor.track_search(
            term = "power drill",
            num_results = 10,
            autocomplete_section = "standard"
        )
        assert resp.status_code == 204
        assert resp.text == ""

    def test_click_through(self):
        constructor = ConstructorIO(
            apiToken = "apiToken",
            autocompleteKey = "autocompleteKey",
            protocol = "http",
            host = "ac.cnstrc.com"
        )
        resp = constructor.track_click_through(
            term = "power drill",
            autocomplete_section = "standard"
        )
        assert resp.status_code == 204
        assert resp.text == ""
