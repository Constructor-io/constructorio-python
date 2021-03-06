import vcr
import requests_mock
from unittest import TestCase

from constructor_io.constructor_io import ConstructorIO, ConstructorError,\
    ConstructorServerError, ConstructorInputError

HTTPS_ARGS = {
    "api_token": "my-api-token",
    "key": "my_api_key",
    "protocol": "https",
    "host": "ac.cnstrc.com"
}

my_vcr = vcr.VCR(record_mode="none", decode_compressed_response=True)

vcr_matchers = ("uri", "method", "body")


class TestConstructorIO(TestCase):
    def test_encodes_parameters(self):
        constructor = ConstructorIO(api_token="boinka",
                                    key="doinka")
        serialized_params = constructor._serialize_params(
            {'foo': [1, 2], 'bar': ['a', 'b']}, sort=True)
        assert serialized_params == 'bar=a&bar=b&foo=1&foo=2'

    def test_key_argument(self):
        # Usual:
        constructor = ConstructorIO(api_token="boinka", key="a")
        self.assertEquals(constructor._key, "a")
        # Backward compatibility:
        constructor = ConstructorIO(api_token="boinka", autocomplete_key="b")
        self.assertEquals(constructor._key, "b")
        # Positional:
        constructor = ConstructorIO("boinka", "c")
        self.assertEquals(constructor._key, "c")
        # Missing:
        with self.assertRaises(TypeError):
            ConstructorIO("boinka")

    def test_creates_urls_correctly(self):
        constructor = ConstructorIO(api_token="boinka",
                                    key="a-test-autocomplete-key")
        generated_url = constructor._make_url('v1/test')
        assert generated_url == 'https://ac.cnstrc.com/v1/test?' \
                                'key=a-test-autocomplete-key'

    def test_set_api_token(self):
        api_token = 'a-test-api-key',
        constructor = ConstructorIO(api_token=api_token,
                                    key="boinka")
        assert constructor._api_token == api_token

    def test_set_ac_key(self):
        key = 'a-test-autocomplete-key'
        constructor = ConstructorIO(key=key,
                                    api_token="boinka")
        assert constructor._key == key

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
        with my_vcr.use_cassette("fixtures/ac.cnstrc.com/add-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            resp = constructor.add(
                item_name="Metadata Example",
                autocomplete_section="Products",
                url="https://metadata.example",
                metadata={"this_key": "this_value"}
            )
            assert resp is True
        with my_vcr.use_cassette("fixtures/ac.cnstrc.com/remove-success.yaml"):
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
        with my_vcr.use_cassette(
                "fixtures/ac.cnstrc.com/add-batch-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            items = [{"item_name": "new item1"}, {"item_name": "new_item2"}]
            resp = constructor.add_batch(
                items=items,
                autocomplete_section="Search Suggestions",
            )
        assert resp is True

    def test_add_or_update_batch(self):
        with my_vcr.use_cassette(
                "fixtures/ac.cnstrc.com/add-batch-success.yaml"):
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

    def test_patch(self):
        with my_vcr.use_cassette("fixtures/ac.cnstrc.com/patch-success.yaml",
                                 match_on=vcr_matchers):
            constructor = ConstructorIO(**HTTPS_ARGS)
            resp = constructor.add(
                item_name="Stanley_Steamer",
                autocomplete_section="Products",
                url="http://stanley.steamer.me",
            )
            assert resp is True

            resp = constructor.patch(
                item_name="Stanley_Steamer",
                suggested_score=100,
                autocomplete_section="Products",
                url="http://stanley.steam.er"
            )
            assert resp is True
            # clean things up so that when we re-run the test we don't
            # get an error when we add it
            resp = constructor.remove(
                item_name="Stanley_Steamer",
                autocomplete_section="Products"
            )
            assert resp is True

    def test_patch_batch(self):
        with my_vcr.use_cassette("fixtures/ac.cnstrc.com/patch-batch-success.yaml",
                                 match_on=vcr_matchers):
            constructor = ConstructorIO(**HTTPS_ARGS)
            resp = constructor.add_batch(
                items=[
                    {"item_name": "Stanley_Steamer", "url": "http://stanley.steamer.me"},
                    {"item_name": "Everest", "group_ids": ["Mountains"]},
                ],
                autocomplete_section="Products",
            )
            assert resp is True

            resp = constructor.patch_batch(
                items=[
                    {"item_name": "Stanley_Steamer", "url": "http://stanley.steam.er"},
                    {"item_name": "Everest", "group_ids": ["Mountains", "High Mountains"]},
                ],
                autocomplete_section="Products",
            )
            assert resp is True
            # clean things up so that when we re-run the test we don't
            # get an error when we add it
            resp = constructor.remove_batch(
                items=[
                    {"item_name": "Stanley_Steamer"},
                    {"item_name": "Everest"},
                ],
                autocomplete_section="Products"
            )
            assert resp is True

    def test_get_refined_queries(self):
        with my_vcr.use_cassette("fixtures/ac.cnstrc.com/get-refined-queries-success.yaml"):
            constructor = ConstructorIO(**HTTPS_ARGS)
            refined_queries = constructor.get_refined_queries(
                query="query_1",
                autocomplete_section="Products"
            )
            assert refined_queries == [
                {
                    "query": "query_1",
                    "whitelist_rule": None,
                    "blacklist_rules": [],
                    "boost_rules": []
                }
            ]

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

    def test_exceptions(self):
        constructor = ConstructorIO(**HTTPS_ARGS)
        with requests_mock.mock() as mock:
            # Test for 400 errors:
            mock.get("https://ac.cnstrc.com/autocomplete/a?key=my_api_key",
                     status_code=403)
            with self.assertRaises(ConstructorInputError):
                constructor.query(query_str="a")

            # Test for 500 errors
            mock.get("https://ac.cnstrc.com/autocomplete/a?key=my_api_key",
                     status_code=500)
            constructor._server_error_retries = 0
            with self.assertRaises(ConstructorServerError):
                constructor.query(query_str="a")

        # Assert exception payload inclusion
        self.assertEquals(str(ConstructorServerError("payload")),
                          "Server error: payload")
        self.assertEquals(str(ConstructorInputError("payload")),
                          "Bad request: payload")
        self.assertEquals(str(ConstructorError("payload")),
                          "Undefined error with Constructor.io: payload")

        # Make sure ConstructorError handling will handle other exceptions
        with self.assertRaises(ConstructorError):
            raise ConstructorServerError()
        with self.assertRaises(ConstructorError):
            raise ConstructorInputError()
