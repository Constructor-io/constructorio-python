import pytest
import constructorio

class something:
    def test_encodes_parameters():
        var constructorio = new Constructorio({})
        assert.equal(constructorio.client._serializeParams({foo: [1, 2], bar: {baz: ['a', 'b']}}), 'foo%5B%5D=1&foo%5B%5D=2&bar%5Bbaz%5D%5B%5D=a&bar%5Bbaz%5D%5B%5D=b')

    def test_creates_urls_correctly():
        var constructorio = new Constructorio({
          autocompleteKey: 'a-test-autocomplete-key',
        })
        assert.equal(constructorio.client._makeUrl('test'), 'https://ac.cnstrc.com/v1/test?autocomplete_key=a-test-autocomplete-key')

    def test_set_api_token():
        var apiToken = 'a-test-api-key',
        constructorio = new Constructorio({ apiToken: apiToken })

        assert.equal(constructorio.config.apiToken, apiToken)

    def test_set_ac_key():
        var autocompleteKey = 'a-test-autocomplete-key',
            constructorio = new Constructorio({ autocompleteKey: autocompleteKey })
        assert.equal(constructorio.config.autocompleteKey, autocompleteKey)

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
