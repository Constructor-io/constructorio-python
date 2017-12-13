import pytest
import vcr
from constructor_io.constructor_io import ConstructorIO, ConstructorError

HTTPS_ARGS = {
    "api_token": "my-api-token",
    "autocomplete_key": "my_api_key",
    "protocol": "https",
    "host": "ac.cnstrc.com"
}

my_vcr = vcr.VCR(record_mode="none")

class TestConstructorIO:
    def test_encodes_parameters(self):
        constructor = ConstructorIO(api_token="boinka",
                                    autocomplete_key="doinka")
        serialized_params = constructor\
            ._serialize_params({'foo': [1, 2], 'bar': {'baz': ['a', 'b']}})
        assert serialized_params == "foo=%5B1%2C+2%5D&bar=%7B%27baz%27%3" \
                                    "A+%5B%27a%27%2C+%27b%27%5D%7D"

    def test_creates_urls_correctly(self):
        constructor = ConstructorIO(api_token="boinka",
                                    autocomplete_key="a-test-autocomplete-key")
        generated_url = constructor._make_url('v1/test')
        assert generated_url == 'https://ac.cnstrc.com/v1/test?' \
                                'autocomplete_key=a-test-autocomplete-key'

    def test_set_api_token(self):
        api_token = 'a-test-api-key',
        constructor = ConstructorIO(api_token=api_token,
                                    autocomplete_key="boinka")
        assert constructor._api_token == api_token

    def test_set_ac_key(self):
        autocomplete_key = 'a-test-autocomplete-key'
        constructor = ConstructorIO(autocomplete_key=autocomplete_key,
                                    api_token="boinka")
        assert constructor._autocomplete_key == autocomplete_key

    def test_ac_query(self):
        with my_vcr.use_cassette("fixtures/ac.cnstrc.com/query-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            autocompletes = constructor.query(
                query_str="a"
            )
            assert autocompletes is not None
            assert type(autocompletes) == dict

    def test_add(self):
        with my_vcr.use_cassette("fixtures/ac.cnstrc.com/add-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            resp = constructor.add(
                item_name="boinkamoinka",
                autocomplete_section="Search Suggestions"
            )
            assert resp is True

    def test_add_remove_metadata(self):
        with my_vcr.use_cassette("fixtures/ac.cnstrc.com/add-metadata-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            resp = constructor.add(
                item_name="Metadata Example",
                autocomplete_section="Products",
                url="https://metadata.example",
                metadata={ "this_key": "this_value" }
            )
            assert resp is True
            resp = constructor.remove(
                item_name="Metadata Example",
                autocomplete_section="Products"
            )
            assert resp is True

    def test_add_or_update(self):
        with my_vcr.use_cassette(
                "fixtures/ac.cnstrc.com/add-update-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            resp = constructor.add_or_update(
                item_name="boinkamoinkar",
                autocomplete_section="Products",
                url="www.googles.com"
            )
            assert resp is True
            resp2 = constructor.add_or_update(
                item_name="boinkamoinkar",
                autocomplete_section="Products",
                url="www.googles1.com"
            )
            assert resp2 is True

    def test_add_batch(self):
        with my_vcr.use_cassette("fixtures/ac.cnstrc.com/add-batch-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            items = [{"item_name": "new item1"}, {"item_name": "new_item2"}]
            resp = constructor.add_batch(
                items=items,
                autocomplete_section="Search Suggestions",
            )
        assert resp is True

    def test_add_or_update_batch(self):
        with my_vcr.use_cassette(
                "fixtures/ac.cnstrc.com/add-or-update-batch-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            items = [{"item_name": "new item", "url": "http://my_url.com"},
                     {"item_name": "new_item2", "url": "http://other_url.com"}]
            resp = constructor.add_or_update_batch(
                items=items,
                autocomplete_section="Products",
            )
            assert resp is True
            items = [{"item_name": "new item", "url": "http://my_url1.com"},
                     {"item_name": "new_item2", "url": "http://other_url.com"},
                     {"item_name": "new_item3", "url": "http://third_url.com"}]
            resp2 = constructor.add_or_update_batch(
                items=items,
                autocomplete_section="Products",
            )
            assert resp2 is True

    def test_remove(self):
        with my_vcr.use_cassette("fixtures/ac.cnstrc.com/remove-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            resp = constructor.remove(
                item_name="boinkamoinka",
                autocomplete_section="Search Suggestions"
            )
            assert resp is True

    def test_remove_batch(self):
        with my_vcr.use_cassette(
                "fixtures/ac.cnstrc.com/remove-batch-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            items = [{"item_name": "new item1"}, {"item_name": "new_item2"}]
            resp = constructor.remove_batch(
                items=items,
                autocomplete_section="Search Suggestions",
            )
        assert resp is True

    def test_modify(self):
        with my_vcr.use_cassette("fixtures/ac.cnstrc.com/modify-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            resp = constructor.add(
                item_name="Stanley_Steamer",
                autocomplete_section="Search Suggestions"
            )
            assert resp is True

            resp = constructor.modify(
                item_name="Stanley_Steamer",
                new_item_name="Newer_Stanley_Steamer",
                suggested_score=100,
                autocomplete_section="Search Suggestions"
            )
            assert resp is True
            # clean things up so that when we re-run the test we don't
            # get an error when we add it
            resp = constructor.remove(
                item_name="Newer_Stanley_Steamer",
                autocomplete_section="Search Suggestions"
            )
            assert resp is True

    def test_conversion(self):
        with my_vcr.use_cassette(
                "fixtures/ac.cnstrc.com/conversion-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            resp = constructor.track_conversion(
                term="Stanley_Steamer",
                autocomplete_section="Search Suggestions"
            )
            assert resp is True

    def test_search_no_num_res(self):
        with my_vcr.use_cassette(
                "fixtures/ac.cnstrc.com/search-noname-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            resp = constructor.track_search(
                term="Stanley_Steamer",
                num_results=10,
                autocomplete_section="Search Suggestions"
            )
            assert resp is True

    def test_search_num_res(self):
        with my_vcr.use_cassette("fixtures/ac.cnstrc.com/search-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            resp = constructor.track_search(
                term="Stanley_Steamer",
                num_results=10,
                autocomplete_section="Search Suggestions"
            )
            assert resp is True

    def test_click_through(self):
        with my_vcr.use_cassette(
                "fixtures/ac.cnstrc.com/click-through-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            resp = constructor.track_click_through(
                term="Stanley_Steamer",
                autocomplete_section="Search Suggestions"
            )
            assert resp is True
