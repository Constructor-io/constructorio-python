'''ConstructorIO Python Client - Autocomplete Tests'''

from os import environ
from unittest import mock

import requests
from pytest import raises

from constructorio_python.constructorio import ConstructorIO
from constructorio_python.helpers.exception import HttpException

test_api_key = environ['TEST_API_KEY']
valid_client_id = '2b23dd74-5672-4379-878c-9182938d2710'
valid_session_id = 2
valid_options = { 'api_key': test_api_key }
query = 'item'

class TestGetAutocompleteResults():
    '''Test get_autocomplete_results'''

    def test_with_valid_query_and_identifiers(self):
        '''Should return a response with a valid query and client + session identifiers'''

        client_session_identifiers = {
            'client_id': valid_client_id,
            'session_id': valid_session_id,
        }
        autocomplete = ConstructorIO(valid_options).autocomplete
        response = autocomplete.get_autocomplete_results(query, {}, {**client_session_identifiers})

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('sections'), dict)
        assert isinstance(response.get('result_id'), str)
        assert response.get('request').get('term') == query


    def test_with_valid_query_and_test_cells(self):
        '''Should return a response with a valid query and test_cells'''

        test_cells = { 'foo': 'bar' }
        autocomplete = ConstructorIO(valid_options).autocomplete
        response = autocomplete.get_autocomplete_results(query, {}, { 'test_cells': test_cells })
        first_key = next(iter(test_cells.keys()))

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('sections'), dict)
        assert isinstance(response.get('result_id'), str)
        assert response.get('request').get(f'ef-{first_key}') == test_cells[first_key]

    def test_with_valid_query_and_segments(self):
        '''Should return a response with a valid query and segments'''

        segments = ['foo', 'bar'];
        autocomplete = ConstructorIO(valid_options).autocomplete
        response = autocomplete.get_autocomplete_results(query, {}, { 'segments': segments })

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('sections'), dict)
        assert isinstance(response.get('result_id'), str)
        assert response.get('request').get('us') == segments

    def test_with_valid_query_and_user_id(self):
        '''Should return a response with a valid query and user_id'''

        user_id = 'user-id'
        autocomplete = ConstructorIO(valid_options).autocomplete
        response = autocomplete.get_autocomplete_results(query, {}, { 'user_id': user_id })

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('sections'), dict)
        assert isinstance(response.get('result_id'), str)

    def test_with_valid_query_and_num_results(self):
        '''Should return a response with a valid query and num_results'''

        num_results = 2
        autocomplete = ConstructorIO(valid_options).autocomplete
        response = autocomplete.get_autocomplete_results(query, { 'num_results': num_results })
        sections = response.get('sections')
        result_count = 0

        for section in sections.values():
            result_count += len(section)

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('sections'), dict)
        assert isinstance(response.get('result_id'), str)
        assert response.get('request').get('num_results') == num_results
        assert result_count == num_results

    def test_with_valid_query_and_results_per_section(self):
        '''Should return a response with a valid query and results_per_section'''

        results_per_section = {
            'Products': 1,
            'Search Suggestions': 2,
        }
        autocomplete = ConstructorIO(valid_options).autocomplete
        response = autocomplete.get_autocomplete_results(query, { 'results_per_section': results_per_section })

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('sections'), dict)
        assert isinstance(response.get('result_id'), str)
        assert response.get('request').get('num_results_Products') == results_per_section.get('Products')
        assert response.get('request').get('num_results_Search Suggestions') == results_per_section.get('Search Suggestions')

    def test_with_valid_query_and_filters(self):
        '''Should return a response with a valid query and filters'''

        filters = { 'keywords': ['battery-powered'] }
        autocomplete = ConstructorIO(valid_options).autocomplete
        response = autocomplete.get_autocomplete_results(query, { 'filters': filters })

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('sections'), dict)
        assert isinstance(response.get('result_id'), str)
        assert response.get('request').get('filters') == filters

    def test_with_valid_query_and_multiple_filters(self):
        '''Should return a response with a valid query and multiple filters'''

        filters = { 'group_id': ['All'], 'Brand': ['XYZ'] }
        autocomplete = ConstructorIO(valid_options).autocomplete
        response = autocomplete.get_autocomplete_results(query, { 'filters': filters })

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('sections'), dict)
        assert isinstance(response.get('result_id'), str)
        assert response.get('request').get('filters') == filters
        assert len(response.get('sections').get('Products')) >= 1

    def test_with_valid_query_and_user_ip(self):
        '''Should return a response with a valid query and user_ip'''

        user_ip = '127.0.0.1'

        with mock.patch.object(requests, 'get', wraps=requests.get) as mockedRequests:
            autocomplete = ConstructorIO({ **valid_options, 'requests': requests }).autocomplete
            response = autocomplete.get_autocomplete_results(query, {}, { 'user_ip': user_ip })
            headers = mockedRequests.call_args.kwargs.get('headers')

            assert isinstance(response.get('request'), dict)
            assert isinstance(response.get('sections'), dict)
            assert isinstance(response.get('result_id'), str)
            assert headers.get('X-Forwarded-For') == user_ip

    def test_with_valid_query_and_security_token(self):
        '''Should return a response with a valid query and security_token'''

        security_token = 'cio-python-test'

        with mock.patch.object(requests, 'get', wraps=requests.get) as mockedRequests:
            autocomplete = ConstructorIO({ **valid_options, 'requests': requests, 'security_token': security_token }).autocomplete
            response = autocomplete.get_autocomplete_results(query)
            headers = mockedRequests.call_args.kwargs.get('headers')

            assert isinstance(response.get('request'), dict)
            assert isinstance(response.get('sections'), dict)
            assert isinstance(response.get('result_id'), str)
            assert headers.get('x-cnstrc-token') == security_token

    def test_with_valid_query_and_user_agent(self):
        '''Should return a response with a valid query and user_agent'''

        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'

        with mock.patch.object(requests, 'get', wraps=requests.get) as mockedRequests:
            autocomplete = ConstructorIO({ **valid_options, 'requests': requests }).autocomplete
            response = autocomplete.get_autocomplete_results(query, {}, { 'user_agent': user_agent })
            headers = mockedRequests.call_args.kwargs.get('headers')

            assert isinstance(response.get('request'), dict)
            assert isinstance(response.get('sections'), dict)
            assert isinstance(response.get('result_id'), str)
            assert headers.get('User-Agent') == user_agent

    def test_with_valid_query_with_result_id(self):
        '''Should return a response with a valid query with a result_id appended to each result'''

        autocomplete = ConstructorIO(valid_options).autocomplete
        response = autocomplete.get_autocomplete_results(query)
        sections = response.get('sections')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('sections'), dict)
        assert isinstance(response.get('result_id'), str)

        for section in sections.values():
            for item in section:
                assert isinstance(item.get('result_id'), str)
                assert item.get('result_id') == response.get('result_id')

    def test_with_valid_query_and_hidden_fields(self):
        '''Should return a response with a valid query and hiddenFields'''

        hidden_fields = ['hidden_field1', 'hidden_field2'];
        autocomplete = ConstructorIO(valid_options).autocomplete
        response = autocomplete.get_autocomplete_results(query, { 'hidden_fields': hidden_fields })

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('sections'), dict)
        assert isinstance(response.get('result_id'), str)
        assert response.get('request').get('hidden_fields') == hidden_fields

    def test_with_invalid_query(self):
        '''Should be rejected when invalid query is provided'''

        with raises(Exception, match=r'query is a required parameter of type string'):
            autocomplete = ConstructorIO(valid_options).autocomplete
            autocomplete.get_autocomplete_results([])

    def test_with_no_query(self):
        '''Should be rejected when no query is provided'''

        with raises(Exception, match=r'query is a required parameter of type string'):
            autocomplete = ConstructorIO(valid_options).autocomplete
            autocomplete.get_autocomplete_results(None)

    def test_with_invalid_num_results(self):
        '''Should be rejected when invalid num_results parameter is provided'''

        with raises(HttpException, match=r'num_results must be an integer'):
            autocomplete = ConstructorIO(valid_options).autocomplete
            autocomplete.get_autocomplete_results(query, { 'num_results': 'abc' })

    def test_with_invalid_filters(self):
        '''Should be rejected when invalid filters parameter is provided'''

        with raises(Exception, match=r'filters must be a dictionary'):
            autocomplete = ConstructorIO(valid_options).autocomplete
            autocomplete.get_autocomplete_results(query, { 'filters': 'abc' })

    def test_with_invalid_api_key(self):
        '''Should be rejected when invalid api_key is provided'''

        with raises(HttpException, match=r'We have no record of this key. You can find your key at app.constructor.io/dashboard.'):
            autocomplete = ConstructorIO({ **valid_options, 'api_key': 'fyzs7tfF8L161VoAXQ8u' }).autocomplete
            autocomplete.get_autocomplete_results(query)

    def test_with_no_api_key(self):
        '''Should be rejected when no api_key is provided'''

        with raises(Exception, match=r'API key is a required parameter of type string'):
            autocomplete = ConstructorIO({}).autocomplete
            autocomplete.get_autocomplete_results(query)
