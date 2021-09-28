'''ConstructorIO Python Client - Autocomplete Tests'''

from os import environ
from unittest import mock

import requests
from pytest import raises

from constructorio_python.constructorio import ConstructorIO
from constructorio_python.helpers.exception import HttpException

test_api_key = environ['TEST_API_KEY']
VALID_CLIENT_ID = '2b23dd74-5672-4379-878c-9182938d2710'
VALID_SESSION_ID = 2
VALID_OPTIONS = { 'api_key': test_api_key }
QUERY = 'item'

def test_with_valid_query_and_identifiers():
    '''Should return a response with a valid query and client + session identifiers'''

    client_session_identifiers = {
        'client_id': VALID_CLIENT_ID,
        'session_id': VALID_SESSION_ID,
    }
    autocomplete = ConstructorIO(VALID_OPTIONS).autocomplete
    response = autocomplete.get_autocomplete_results(QUERY, {}, {**client_session_identifiers})

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('sections'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('term') == QUERY


def test_with_valid_query_and_test_cells():
    '''Should return a response with a valid query and test_cells'''

    test_cells = { 'foo': 'bar' }
    autocomplete = ConstructorIO(VALID_OPTIONS).autocomplete
    response = autocomplete.get_autocomplete_results(QUERY, {}, { 'test_cells': test_cells })
    first_key = next(iter(test_cells.keys()))

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('sections'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get(f'ef-{first_key}') == test_cells[first_key]

def test_with_valid_query_and_segments():
    '''Should return a response with a valid query and segments'''

    segments = ['foo', 'bar']
    autocomplete = ConstructorIO(VALID_OPTIONS).autocomplete
    response = autocomplete.get_autocomplete_results(QUERY, {}, { 'segments': segments })

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('sections'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('us') == segments

def test_with_valid_query_and_user_id():
    '''Should return a response with a valid query and user_id'''

    user_id = 'user-id'
    autocomplete = ConstructorIO(VALID_OPTIONS).autocomplete
    response = autocomplete.get_autocomplete_results(QUERY, {}, { 'user_id': user_id })

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('sections'), dict)
    assert isinstance(response.get('result_id'), str)

def test_with_valid_query_and_num_results():
    '''Should return a response with a valid query and num_results'''

    num_results = 2
    autocomplete = ConstructorIO(VALID_OPTIONS).autocomplete
    response = autocomplete.get_autocomplete_results(QUERY, { 'num_results': num_results })
    sections = response.get('sections')
    result_count = 0

    for section in sections.values():
        result_count += len(section)

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('sections'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('num_results') == num_results
    assert result_count == num_results

def test_with_valid_query_and_results_per_section():
    '''Should return a response with a valid query and results_per_section'''

    results_per_section = {
        'Products': 1,
        'Search Suggestions': 2,
    }
    autocomplete = ConstructorIO(VALID_OPTIONS).autocomplete
    response = autocomplete.get_autocomplete_results(
        QUERY,
        { 'results_per_section': results_per_section }
    )
    num_results_products = response.get('request').get('num_results_Products')
    num_results_search_suggestions = response.get('request').get('num_results_Search Suggestions')

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('sections'), dict)
    assert isinstance(response.get('result_id'), str)
    assert num_results_products == results_per_section.get('Products')
    assert num_results_search_suggestions == results_per_section.get('Search Suggestions')

def test_with_valid_query_and_filters():
    '''Should return a response with a valid query and filters'''

    filters = { 'keywords': ['battery-powered'] }
    autocomplete = ConstructorIO(VALID_OPTIONS).autocomplete
    response = autocomplete.get_autocomplete_results(QUERY, { 'filters': filters })

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('sections'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('filters') == filters

def test_with_valid_query_and_multiple_filters():
    '''Should return a response with a valid query and multiple filters'''

    filters = { 'group_id': ['All'], 'Brand': ['XYZ'] }
    autocomplete = ConstructorIO(VALID_OPTIONS).autocomplete
    response = autocomplete.get_autocomplete_results(QUERY, { 'filters': filters })

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('sections'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('filters') == filters
    assert len(response.get('sections').get('Products')) >= 1

def test_with_valid_query_and_user_ip():
    '''Should return a response with a valid query and user_ip'''

    user_ip = '127.0.0.1'

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        autocomplete = ConstructorIO({ **VALID_OPTIONS, 'requests': requests }).autocomplete
        response = autocomplete.get_autocomplete_results(QUERY, {}, { 'user_ip': user_ip })
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('sections'), dict)
        assert isinstance(response.get('result_id'), str)
        assert headers.get('X-Forwarded-For') == user_ip

def test_with_valid_query_and_security_token():
    '''Should return a response with a valid query and security_token'''

    security_token = 'cio-python-test'

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        autocomplete = ConstructorIO({
            **VALID_OPTIONS,
            'requests': requests,
            'security_token': security_token
        }).autocomplete
        response = autocomplete.get_autocomplete_results(QUERY)
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('sections'), dict)
        assert isinstance(response.get('result_id'), str)
        assert headers.get('x-cnstrc-token') == security_token

def test_with_valid_query_and_user_agent():
    '''Should return a response with a valid query and user_agent'''

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36' # pylint: disable=line-too-long

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        autocomplete = ConstructorIO({ **VALID_OPTIONS, 'requests': requests }).autocomplete
        response = autocomplete.get_autocomplete_results(QUERY, {}, { 'user_agent': user_agent })
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('sections'), dict)
        assert isinstance(response.get('result_id'), str)
        assert headers.get('User-Agent') == user_agent

def test_with_valid_query_with_result_id():
    '''Should return a response with a valid query with a result_id appended to each result'''

    autocomplete = ConstructorIO(VALID_OPTIONS).autocomplete
    response = autocomplete.get_autocomplete_results(QUERY)
    sections = response.get('sections')

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('sections'), dict)
    assert isinstance(response.get('result_id'), str)

    for section in sections.values():
        for item in section:
            assert isinstance(item.get('result_id'), str)
            assert item.get('result_id') == response.get('result_id')

def test_with_valid_query_and_hidden_fields():
    '''Should return a response with a valid query and hiddenFields'''

    hidden_fields = ['hidden_field1', 'hidden_field2']
    autocomplete = ConstructorIO(VALID_OPTIONS).autocomplete
    response = autocomplete.get_autocomplete_results(QUERY, { 'hidden_fields': hidden_fields })

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('sections'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('hidden_fields') == hidden_fields

def test_with_invalid_query():
    '''Should be rejected when invalid query is provided'''

    with raises(Exception, match=r'query is a required parameter of type string'):
        autocomplete = ConstructorIO(VALID_OPTIONS).autocomplete
        autocomplete.get_autocomplete_results([])

def test_with_no_query():
    '''Should be rejected when no query is provided'''

    with raises(Exception, match=r'query is a required parameter of type string'):
        autocomplete = ConstructorIO(VALID_OPTIONS).autocomplete
        autocomplete.get_autocomplete_results(None)

def test_with_invalid_num_results():
    '''Should be rejected when invalid num_results parameter is provided'''

    with raises(HttpException, match=r'num_results must be an integer'):
        autocomplete = ConstructorIO(VALID_OPTIONS).autocomplete
        autocomplete.get_autocomplete_results(QUERY, { 'num_results': 'abc' })

def test_with_invalid_filters():
    '''Should be rejected when invalid filters parameter is provided'''

    with raises(Exception, match=r'filters must be a dictionary'):
        autocomplete = ConstructorIO(VALID_OPTIONS).autocomplete
        autocomplete.get_autocomplete_results(QUERY, { 'filters': 'abc' })

def test_with_invalid_api_key():
    '''Should be rejected when invalid api_key is provided'''

    with raises(
            HttpException,
            match=r'We have no record of this key. You can find your key at app.constructor.io/dashboard.' # pylint: disable=line-too-long
    ):
        autocomplete = ConstructorIO({
            **VALID_OPTIONS,
            'api_key': 'fyzs7tfF8L161VoAXQ8u'
        }).autocomplete
        autocomplete.get_autocomplete_results(QUERY)

def test_with_no_api_key():
    '''Should be rejected when no api_key is provided'''

    with raises(Exception, match=r'API key is a required parameter of type string'):
        autocomplete = ConstructorIO({}).autocomplete
        autocomplete.get_autocomplete_results(QUERY)
