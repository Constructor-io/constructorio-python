'''ConstructorIO Python Client - Search Tests'''

import re
from os import environ
from unittest import mock

import requests
from pytest import raises

from constructor_io.constructor_io import ConstructorIO
from constructor_io.helpers.exception import (ConstructorException,
                                              HttpException)

TEST_API_KEY = environ['TEST_REQUEST_API_KEY']
VALID_CLIENT_ID = '2b23dd74-5672-4379-878c-9182938d2710'
VALID_SESSION_ID = 2
VALID_OPTIONS = { 'api_key': TEST_API_KEY }
QUERY = 'item'
SECTION = 'Products'

def test_with_valid_query_and_identifiers():
    '''Should return a response with a valid query, section, and client + session identifiers'''

    client_session_identifiers = {
        'client_id': VALID_CLIENT_ID,
        'session_id': VALID_SESSION_ID,
    }
    search = ConstructorIO(VALID_OPTIONS).search
    response = search.get_search_results(
        QUERY,
        { 'section': SECTION },
        {**client_session_identifiers}
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('term') == QUERY
    assert response.get('request').get('section') == SECTION
    assert isinstance(response.get('response').get('results'), list)

def test_with_valid_query_and_test_cells():
    '''Should return a response with a valid query, section, and test_cells'''

    test_cells = { 'foo': 'bar' }
    search = ConstructorIO(VALID_OPTIONS).search
    response = search.get_search_results(
        QUERY,
        { 'section': SECTION },
        { 'test_cells': test_cells }
    )
    first_key = next(iter(test_cells.keys()))

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get(f'ef-{first_key}') == test_cells[first_key]

def test_with_valid_query_and_segments():
    '''Should return a response with a valid query, section, and segments'''

    segments = ['foo', 'bar']
    search = ConstructorIO(VALID_OPTIONS).search
    response = search.get_search_results(QUERY, { 'section': SECTION }, { 'segments': segments })

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('us') == segments

def test_with_valid_query_and_user_id():
    '''Should return a response with a valid query, section, and user_id'''

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        user_id = 'user-id'
        search = ConstructorIO({ **VALID_OPTIONS, 'requests': requests }).search
        response = search.get_search_results(QUERY, { 'section': SECTION }, { 'user_id': user_id })
        request_url = mocked_requests.call_args.args[0]

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert re.search('ui=user-id', request_url)

def test_with_valid_query_and_page():
    '''Should return a response with a valid query, section, and page'''

    page = 1
    search = ConstructorIO(VALID_OPTIONS).search
    response = search.get_search_results(QUERY, { 'section': SECTION, 'page': page })

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('page') == page

def test_with_valid_query_and_results_per_page():
    '''Should return a response with a valid query, section, and results_per_page'''

    results_per_page = 2
    search = ConstructorIO(VALID_OPTIONS).search
    response = search.get_search_results(
        QUERY,
        { 'results_per_page': results_per_page }
    )
    num_results = response.get('request').get('num_results_per_page')

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert num_results == results_per_page

def test_with_valid_query_and_filters():
    '''Should return a response with a valid query, section, and filters'''

    filters = { 'keywords': ['battery-powered'] }
    search = ConstructorIO(VALID_OPTIONS).search
    response = search.get_search_results(QUERY, { 'section': SECTION, 'filters': filters })

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('filters') == filters

def test_with_valid_query_and_fmt_options():
    '''Should return a response with a valid query, section, and fmt_options'''

    fmt_options = { 'groups_max_depth': 2, 'groups_start': 'current' }
    search = ConstructorIO(VALID_OPTIONS).search
    response = search.get_search_results(QUERY, { 'section': SECTION, 'fmt_options': fmt_options })

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('fmt_options').get('groups_max_depth') == 2
    assert response.get('request').get('fmt_options').get('groups_start') == 'current'

def test_with_valid_query_and_sort_by():
    '''Should return a response with a valid query, section, and sort_by'''

    sort_by = 'relevance'
    search = ConstructorIO(VALID_OPTIONS).search
    response = search.get_search_results(QUERY, { 'section': SECTION, 'sort_by': sort_by })

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('sort_by') == sort_by

def test_with_valid_query_and_sort_order():
    '''Should return a response with a valid query, section, and sort_by'''

    sort_order = 'ascending'
    search = ConstructorIO(VALID_OPTIONS).search
    response = search.get_search_results(QUERY, { 'section': SECTION, 'sort_order': sort_order })

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('sort_order') == sort_order

def test_with_valid_query_and_user_ip():
    '''Should return a response with a valid query, section, and user_ip'''

    user_ip = '127.0.0.1'

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        search = ConstructorIO({ **VALID_OPTIONS, 'requests': requests }).search
        response = search.get_search_results(QUERY, { 'section': SECTION }, { 'user_ip': user_ip })
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert headers.get('X-Forwarded-For') == user_ip

def test_with_valid_query_and_security_token():
    '''Should return a response with a valid query, section, and security_token'''

    security_token = 'cio-python-test'

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        search = ConstructorIO({
            **VALID_OPTIONS,
            'requests': requests,
            'security_token': security_token
        }).search
        response = search.get_search_results(QUERY, { 'section': SECTION })
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert headers.get('x-cnstrc-token') == security_token

def test_with_valid_query_and_user_agent():
    '''Should return a response with a valid query, section, and user_agent'''

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36' # pylint: disable=line-too-long

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        search = ConstructorIO({ **VALID_OPTIONS, 'requests': requests }).search
        response = search.get_search_results(
            QUERY,
            { 'section': SECTION },
            { 'user_agent': user_agent }
        )
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert headers.get('User-Agent') == user_agent

def test_with_valid_query_with_result_id():
    '''Should return a response with a valid query and section with a result_id appended to each result''' # pylint: disable=line-too-long

    search = ConstructorIO(VALID_OPTIONS).search
    response = search.get_search_results(QUERY, { 'section': SECTION })

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('results'), list)

    for result in response.get('response').get('results'):
        assert isinstance(result.get('result_id'), str)
        assert result.get('result_id') == response.get('result_id')

def test_with_valid_query_and_hidden_fields():
    '''Should return a response with a valid query, section, and hiddenFields'''

    hidden_fields = ['hidden_field1', 'hidden_field2']
    search = ConstructorIO(VALID_OPTIONS).search
    response = search.get_search_results(
        QUERY,
        { 'section': SECTION, 'hidden_fields': hidden_fields }
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('fmt_options').get('hidden_fields') == hidden_fields

def test_with_valid_query_and_hidden_facets():
    '''Should return a response with a valid query, section, and hiddenFacets'''

    hidden_facets = ['Brand', 'testFacet']
    search = ConstructorIO(VALID_OPTIONS).search
    response = search.get_search_results(
        'Item1',
        { 'section': SECTION, 'hidden_facets': hidden_facets }
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('fmt_options').get('hidden_facets') == hidden_facets
    facets = response.get('response').get('facets')
    brand_facet = None

    try:
        # Find the element in the list that has the name "Brand"
        brand_facet = next(x for x in facets if x['name'] == hidden_facets[0])
    except StopIteration:
        # Element not found
        pass

    assert brand_facet is not None

def test_with_valid_query_and_redirect_rule():
    '''Should return a redirect rule with a valid query and section'''

    redirect_query = 'rolling'
    search = ConstructorIO(VALID_OPTIONS).search
    response = search.get_search_results(redirect_query, { 'section': SECTION })

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert redirect_query in response.get('response').get('redirect').get('matched_terms')
    assert response.get('response').get('redirect').get('data').get('url') is not None

def test_with_valid_query_and_variations_map():
    '''Should return a response with a valid query, section, and variations_map'''

    variations_map = {
        'group_by': [
            {
                'name': 'variation',
                'field': 'data.variation_id',
            },
        ],
        'values': {
            'size': {
                'aggregation': 'all',
                'field': 'data.facets.size',
                },
            },
        'dtype': 'array',
    }
    search = ConstructorIO(VALID_OPTIONS).search
    response = search.get_search_results(
        'jacket',
        { 'section': SECTION, 'variations_map': variations_map }
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('variations_map') == variations_map
    assert response.get('response').get('results')[0].get('variations_map')[0].get('size') is not None
    assert response.get('response').get('results')[0].get('variations_map')[0].get('variation') is not None

def test_with_invalid_query():
    '''Should raise exception when invalid query is provided'''

    with raises(ConstructorException, match=r'query is a required parameter of type string'):
        search = ConstructorIO(VALID_OPTIONS).search
        search.get_search_results([], { 'section': SECTION })

def test_with_no_query():
    '''Should raise exception when no query is provided'''

    with raises(ConstructorException, match=r'query is a required parameter of type string'):
        search = ConstructorIO(VALID_OPTIONS).search
        search.get_search_results(None, { 'section': SECTION })

def test_with_invalid_page():
    '''Should raise exception when invalid page parameter is provided'''

    with raises(HttpException, match=r'page: value is not a valid integer'):
        search = ConstructorIO(VALID_OPTIONS).search
        search.get_search_results(QUERY, { 'section': SECTION, 'page': 'abc' })

def test_with_invalid_results_per_page():
    '''Should raise exception when invalid results_per_page parameter is provided'''

    with raises(HttpException, match=r'num_results_per_page: value is not a valid integer'):
        search = ConstructorIO(VALID_OPTIONS).search
        search.get_search_results(QUERY, { 'section': SECTION, 'results_per_page': 'abc' })

def test_with_invalid_filters():
    '''Should raise exception when invalid filters parameter is provided'''

    with raises(ConstructorException, match=r'filters must be a dictionary'):
        search = ConstructorIO(VALID_OPTIONS).search
        search.get_search_results(QUERY, { 'section': SECTION, 'filters': 'abc' })

def test_with_invalid_sort_by():
    '''Should raise exception when invalid sort_by parameter is provided'''

    with raises(HttpException, match=r'sort_by: str type expected'):
        search = ConstructorIO(VALID_OPTIONS).search
        search.get_search_results(QUERY, { 'section': SECTION, 'sort_by': ['foo', 'bar'] })

def test_with_invalid_sort_order():
    '''Should raise exception when invalid sort_order parameter is provided'''

    with raises(HttpException, match=r"sort_order: value is not a valid enumeration member; permitted: 'ascending', 'descending'"):
        search = ConstructorIO(VALID_OPTIONS).search
        search.get_search_results(QUERY, { 'section': SECTION, 'sort_order': 123 })

def test_with_invalid_section():
    '''Should raise exception when invalid section parameter is provided'''

    with raises(HttpException, match=r'Unknown section: 123'):
        search = ConstructorIO(VALID_OPTIONS).search
        search.get_search_results(QUERY, { 'section': 123 })

def test_with_invalid_api_key():
    '''Should raise exception when invalid api_key is provided'''

    with raises(
            HttpException,
            match=r'You have supplied an invalid `key` or `autocomplete_key`. You can find your key at app.constructor.io/dashboard/accounts/api_integration.' # pylint: disable=line-too-long
    ):
        search = ConstructorIO({
            **VALID_OPTIONS,
            'api_key': 'fyzs7tfF8L161VoAXQ8u'
        }).search
        search.get_search_results(QUERY, { 'section': SECTION })

def test_with_no_api_key():
    '''Should raise exception when no api_key is provided'''

    with raises(ConstructorException, match=r'API key is a required parameter of type string'):
        search = ConstructorIO({}).search
        search.get_search_results(QUERY)
