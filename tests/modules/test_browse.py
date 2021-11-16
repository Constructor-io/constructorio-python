'''ConstructorIO Python Client - Search Tests''' # pylint: disable=too-many-lines

import re
from os import environ
from unittest import mock

import requests
from pytest import raises

from constructor_io.constructor_io import ConstructorIO

TEST_API_KEY = environ['TEST_API_KEY']
TEST_API_TOKEN = environ['TEST_API_TOKEN']
VALID_CLIENT_ID = '2b23dd74-5672-4379-878c-9182938d2710'
VALID_SESSION_ID = 2
VALID_OPTIONS = {'api_key': TEST_API_KEY}
FILTER_NAME = 'group_id'
FILTER_VALUE = 'Brands'
SECTION = 'Products'
USER_ID = 'user-id'
IDS = ['10001', '10002']


def test_get_browse_results_with_valid_filter_name_filter_value_and_identifiers():
    '''Should return a response with a valid filter_name, filter_value, section, and client + session identifiers''' # pylint: disable=line-too-long

    client_session_identifiers = {
        'client_id': VALID_CLIENT_ID,
        'session_id': VALID_SESSION_ID,
    }
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results(
        FILTER_NAME,
        FILTER_VALUE,
        {'section': SECTION},
        {**client_session_identifiers}
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('browse_filter_name') == FILTER_NAME
    assert response.get('request').get('browse_filter_value') == FILTER_VALUE
    assert response.get('request').get('section') == SECTION
    assert isinstance(response.get('response').get('results'), list)


def test_get_browse_results_with_valid_filter_name_filter_value_and_test_cells():
    '''Should return a response with a valid filter_name, filter_value, section, and test_cells'''

    test_cells = {'foo': 'bar'}
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results(
        FILTER_NAME,
        FILTER_VALUE,
        {'section': SECTION},
        {'test_cells': test_cells}
    )
    first_key = next(iter(test_cells.keys()))

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get(
        f'ef-{first_key}') == test_cells[first_key]


def test_get_browse_results_with_valid_filter_name_filter_value_and_segments():
    '''Should return a response with a valid filter_name, filter_value, section, and segments'''

    segments = ['foo', 'bar']
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results(
        FILTER_NAME,
        FILTER_VALUE,
        {'section': SECTION},
        {'segments': segments}
        )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('us') == segments


def test_get_browse_results_with_valid_filter_name_filter_value_and_user_id():
    '''Should return a response with a valid filter_name, filter_value, section, and user_id'''

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        browse = ConstructorIO({**VALID_OPTIONS, 'requests': requests}).browse
        response = browse.get_browse_results(
            FILTER_NAME,
            FILTER_VALUE,
            {'section': SECTION},
            {'user_id': USER_ID})
        request_url = mocked_requests.call_args.args[0]

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert re.search('ui=user-id', request_url)


def test_get_browse_results_with_valid_filter_name_filter_value_and_page():
    '''Should return a response with a valid filter_name, filter_value, section, and page'''

    page = 1
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results(
        FILTER_NAME,
        FILTER_VALUE,
        {'section': SECTION,'page': page})

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('page') == page


def test_get_browse_results_with_valid_filter_name_filter_value_and_results_per_page():
    '''Should return a response with a valid filter_name, filter_value, section, and results_per_page''' # pylint: disable=line-too-long

    results_per_page = 2
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results(
        FILTER_NAME,
        FILTER_VALUE,
        {'results_per_page': results_per_page}
    )
    num_results = response.get('request').get('num_results_per_page')

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert num_results == results_per_page


def test_get_browse_results_with_valid_filter_name_filter_value_and_filters():
    '''Should return a response with a valid filter_name, filter_value, section, and filters'''

    filters = {'keywords': ['battery-powered']}
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results(
        FILTER_NAME,
        FILTER_VALUE,
        {'section': SECTION, 'filters': filters})

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('filters') == filters


def test_get_browse_results_with_valid_filter_name_filter_value_and_fmt_options():
    '''Should return a response with a valid filter_name, filter_value, section, and fmt_options'''

    fmt_options = {'groups_max_depth': 2, 'groups_start': 'current'}
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results(
        FILTER_NAME,
        FILTER_VALUE,
        {'section': SECTION, 'fmt_options': fmt_options})

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('fmt_options') == fmt_options


def test_get_browse_results_with_valid_filter_name_filter_value_and_sort_by():
    '''Should return a response with a valid filter_name, filter_value, section, and sort_by'''

    sort_by = 'relevance'
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results(
        FILTER_NAME,
        FILTER_VALUE,
        {'section': SECTION, 'sort_by': sort_by})

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('sort_by') == sort_by


def test_get_browse_results_with_valid_filter_name_filter_value_and_sort_order():
    '''Should return a response with a valid filter_name, filter_value, section, and sort_by'''

    sort_order = 'ascending'
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results(
        FILTER_NAME,
        FILTER_VALUE,
        {'section': SECTION, 'sort_order': sort_order})

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('sort_order') == sort_order


def test_get_browse_results_with_valid_filter_name_filter_value_and_user_ip():
    '''Should return a response with a valid filter_name, filter_value, section, and user_ip'''

    user_ip = '127.0.0.1'

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        browse = ConstructorIO({**VALID_OPTIONS, 'requests': requests}).browse
        response = browse.get_browse_results(
            FILTER_NAME,
            FILTER_VALUE,
            {'section': SECTION},
            {'user_ip': user_ip})
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert headers.get('X-Forwarded-For') == user_ip


def test_get_browse_results_with_valid_filter_name_filter_value_and_security_token():
    '''Should return a response with a valid filter_name, filter_value, section, and security_token''' # pylint: disable=line-too-long

    security_token = 'cio-python-test'

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        browse = ConstructorIO({
            **VALID_OPTIONS,
            'requests': requests,
            'security_token': security_token
        }).browse
        response = browse.get_browse_results(
            FILTER_NAME,
            FILTER_VALUE,
            {'section': SECTION})
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert headers.get('x-cnstrc-token') == security_token


def test_get_browse_results_with_valid_filter_name_filter_value_and_user_agent():
    '''Should return a response with a valid filter_name, filter_value, section, and user_agent'''

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'  # pylint: disable=line-too-long

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        browse = ConstructorIO({**VALID_OPTIONS, 'requests': requests}).browse
        response = browse.get_browse_results(
            FILTER_NAME,
            FILTER_VALUE,
            {'section': SECTION},
            {'user_agent': user_agent}
        )
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert headers.get('User-Agent') == user_agent


def test_get_browse_results_with_valid_filter_name_filter_value_with_result_id():
    '''Should return a response with a valid filter_name, filter_value, and section with a result_id appended to each result'''  # pylint: disable=line-too-long

    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results(
        FILTER_NAME,
        FILTER_VALUE,
        {'section': SECTION})

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('results'), list)

    for result in response.get('response').get('results'):
        assert isinstance(result.get('result_id'), str)
        assert result.get('result_id') == response.get('result_id')


def test_get_browse_results_with_valid_filter_name_filter_value_and_hidden_fields():
    '''Should return a response with a valid filter_name, filter_value, section, and hiddenFields''' # pylint: disable=line-too-long

    hidden_fields = ['hidden_field1', 'hidden_field2']
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results(
        FILTER_NAME,
        FILTER_VALUE,
        {'section': SECTION, 'hidden_fields': hidden_fields}
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('hidden_fields') == hidden_fields


def test_get_browse_results_with_invalid_filter_name():
    '''Should raise exception when invalid filter_name is provided'''

    with raises(Exception, match=r'filter_name is a required parameter of type string'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results([], FILTER_VALUE)


def test_get_browse_results_with_invalid_filter_value():
    '''Should raise exception when invalid filter_value is provided'''

    with raises(Exception, match=r'filter_value is a required parameter of type string'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results(FILTER_NAME, [])


def test_get_browse_results_with_no_filter_name():
    '''Should raise exception when no filter_name is provided'''

    with raises(Exception, match=r'filter_name is a required parameter of type string'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results(None, FILTER_VALUE)


def test_get_browse_results_with_no_filter_value():
    '''Should raise exception when no filter_value is provided'''

    with raises(Exception, match=r'filter_value is a required parameter of type string'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results(FILTER_NAME, None)


def test_get_browse_results_with_invalid_page():
    '''Should raise exception when invalid page parameter is provided'''

    with raises(Exception, match=r'page must be an integer'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results(
            FILTER_NAME,
            FILTER_VALUE,
            {'section': SECTION, 'page': 'abc'})


def test_get_browse_results_with_invalid_results_per_page():
    '''Should raise exception when invalid results_per_page parameter is provided'''

    with raises(Exception, match=r'num_results_per_page must be an integer'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results(
            FILTER_NAME,
            FILTER_VALUE,
            {'section': SECTION, 'results_per_page': 'abc'})


def test_get_browse_results_with_invalid_filters():
    '''Should raise exception when invalid filters parameter is provided'''

    with raises(Exception, match=r'filters must be a dictionary'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results(
            FILTER_NAME,
            FILTER_VALUE,
            {'section': SECTION, 'filters': 'abc'})


def test_get_browse_results_with_invalid_sort_by():
    '''Should raise exception when invalid sort_by parameter is provided'''

    with raises(Exception, match=r'sort_by must be a string'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results(
            FILTER_NAME,
            FILTER_VALUE,
            {'section': SECTION, 'sort_by': ['foo', 'bar']})


def test_get_browse_results_with_invalid_sort_order():
    '''Should raise exception when invalid sort_order parameter is provided'''

    with raises(Exception, match=r'Invalid value for parameter: "sort_order"'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results(
            FILTER_NAME,
            FILTER_VALUE,
            {'section': SECTION, 'sort_order': 123})


def test_get_browse_results_with_invalid_section():
    '''Should raise exception when invalid section parameter is provided'''

    with raises(Exception, match=r'Unknown section: 123'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results(
            FILTER_NAME,
            FILTER_VALUE,
            {'section': 123})


def test_get_browse_results_with_invalid_fmt_options():
    '''Should raise exception when invalid fmt_options parameter is provided'''

    with raises(Exception, match=r'fmt_options must be a dictionary'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results(
            FILTER_NAME,
            FILTER_VALUE,
            {'fmt_options': 'abc'})


def test_get_browse_results_with_invalid_api_key():
    '''Should raise exception when invalid api_key is provided'''

    with raises(
            Exception,
            match=r'We have no record of this key. You can find your key at app.constructor.io/dashboard.'  # pylint: disable=line-too-long
    ):
        browse = ConstructorIO({
            **VALID_OPTIONS,
            'api_key': 'fyzs7tfF8L161VoAXQ8u'
        }).browse
        browse.get_browse_results(
            FILTER_NAME,
            FILTER_VALUE,
            {'section': SECTION})


def test_get_browse_results_with_no_api_key():
    '''Should raise exception when no api_key is provided'''

    with raises(Exception, match=r'API key is a required parameter of type string'):
        browse = ConstructorIO({}).browse
        browse.get_browse_results(FILTER_NAME, FILTER_VALUE)


def test_get_browse_groups_without_additional_arguments():
    '''Should return a response without additional arguments'''

    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_groups()

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('groups'), list)


def test_get_browse_groups_with_valid_identifiers():
    '''Should return a response with valid client + session identifiers'''

    client_session_identifiers = {
        'client_id': VALID_CLIENT_ID,
        'session_id': VALID_SESSION_ID,
    }
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_groups(
        {},
        {**client_session_identifiers}
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('groups'), list)


def test_get_browse_groups_with_valid_user_id():
    '''Should return a response with a valid user id'''

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        browse = ConstructorIO(VALID_OPTIONS).browse
        response = browse.get_browse_groups(
            {},
            {'user_id': USER_ID}
        )
        request_url = mocked_requests.call_args.args[0]

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert isinstance(response.get('response').get('groups'), list)
        assert re.search('ui=user-id', request_url)


def test_get_browse_groups_with_valid_filters():
    '''Should return a response with valid filters'''

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        filters = {'group_id': FILTER_VALUE}
        browse = ConstructorIO(VALID_OPTIONS).browse
        response = browse.get_browse_groups(
            { 'filters': filters },
        )
        request_url = mocked_requests.call_args.args[0]

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert isinstance(response.get('response').get('groups'), list)
        assert isinstance(response.get('request').get('filters'), dict)
        assert re.search('filters', request_url)


def test_get_browse_groups_with_valid_fmt_options():
    '''Should return a response with valid fmt_options'''

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        browse = ConstructorIO(VALID_OPTIONS).browse
        response = browse.get_browse_groups(
            { 'fmt_options': { 'groups_max_depth': 4 } },
        )
        request_url = mocked_requests.call_args.args[0]

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert isinstance(response.get('response').get('groups'), list)
        assert isinstance(response.get('request').get('fmt_options'), dict)
        assert isinstance(response.get('request').get('fmt_options').get('groups_max_depth'), int)
        assert re.search('fmt_options%5Bgroups_max_depth', request_url)


def test_get_browse_groups_with_invalid_filters():
    '''Should return a response with invalid filters'''

    with raises(Exception, match=r'filters must be a dictionary'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_groups(
            { 'filters': 123},
        )


def test_get_browse_groups_with_invalid_fmt_options():
    '''Should return a response with invalid fmt_options'''

    with raises(Exception, match=r'fmt_options must be a dictionary'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_groups(
            { 'fmt_options': 123},
        )


def test_get_browse_groups_with_invalid_api_key():
    '''Should return a response with invalid api_key'''

    with raises(Exception, match=r'We have no record of this key. You can find your key at app.constructor.io/dashboard.'): # pylint: disable=line-too-long
        browse = ConstructorIO({'api_key': 'fyzs7tfF8L161VoAXQ8u'}).browse
        browse.get_browse_groups()


def test_get_browse_facets_without_additional_arguments():
    '''Should return a response without additional arguments'''

    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_facets()

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('facets'), list)
    assert isinstance(response.get('response').get('total_num_results'), int)


def test_get_browse_facets_with_valid_page_and_results_per_page():
    '''Should return a response with valid page and results_per_page'''

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        browse = ConstructorIO(VALID_OPTIONS).browse
        response = browse.get_browse_facets(
            { 'page': 2, 'results_per_page': 5 },
        )
        request_url = mocked_requests.call_args.args[0]

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert isinstance(response.get('response').get('facets'), list)
        assert isinstance(response.get('response').get('total_num_results'), int)
        assert isinstance(response.get('request').get('page'), int)
        assert isinstance(response.get('request').get('num_results_per_page'), int)
        assert re.search('page=2', request_url)
        assert re.search('num_results_per_page=5', request_url)


def test_get_browse_facets_with_valid_fmt_options():
    '''Should return a response with valid fmt_options'''

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        browse = ConstructorIO({ **VALID_OPTIONS, 'api_token': TEST_API_TOKEN }).browse
        response = browse.get_browse_facets(
            {
                'fmt_options': { 'show_hidden_facets': True,
                'show_protected_facets': True }
            }
        )
        request_url = mocked_requests.call_args.args[0]

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert isinstance(response.get('response').get('facets'), list)
        assert isinstance(response.get('response').get('total_num_results'), int)
        assert isinstance(response.get('request').get('fmt_options'), dict)
        assert isinstance(response.get('request').get('fmt_options').get('show_hidden_facets'), bool) # pylint: disable=line-too-long
        assert isinstance(response.get('request').get('fmt_options').get('show_protected_facets'), bool) # pylint: disable=line-too-long
        assert re.search('%5Bshow_hidden_facets%5D=True', request_url)
        assert re.search('%5Bshow_protected_facets%5D=True', request_url)


def test_get_browse_facets_with_invalid_page():
    '''Should return a response with invalid page'''

    with raises(Exception, match=r'page must be an integer'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_facets(
            { 'page': 'abc'},
        )


def test_get_browse_facets_with_invalid_results_per_page():
    '''Should return a response with invalid results_per_page'''

    with raises(Exception, match=r'results_per_page must be an integer'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_facets(
            { 'results_per_page': 'abc'},
        )


def test_get_browse_facets_with_invalid_fmt_options():
    '''Should return a response with invalid fmt_options'''

    with raises(Exception, match=r'fmt_options must be a dictionary'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_facets(
            { 'fmt_options': 123},
        )


def test_get_browse_facets_with_invalid_api_key():
    '''Should return a response with invalid api_key'''

    with raises(Exception, match=r'We have no record of this key. You can find your key at app.constructor.io/dashboard.'): # pylint: disable=line-too-long
        browse = ConstructorIO({'api_key': 'fyzs7tfF8L161VoAXQ8u'}).browse
        browse.get_browse_facets()


def test_get_browse_results_for_item_ids_without_additional_arguments():
    '''Should return a response with valid ids'''

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        browse = ConstructorIO(VALID_OPTIONS).browse
        response = browse.get_browse_results_for_item_ids(IDS)
        request_url = mocked_requests.call_args.args[0]

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert isinstance(response.get('response').get('results'), list)
        assert isinstance(response.get('response').get('total_num_results'), int)
        assert re.search('ids=10001&ids=10002', request_url)


def test_get_browse_results_for_item_ids_with_valid_item_ids_and_test_cells():
    '''Should return a response with a valid ids and test_cells'''

    test_cells = {'foo': 'bar'}
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results_for_item_ids(
        IDS,
        {},
        {'test_cells': test_cells})
    first_key = next(iter(test_cells.keys()))

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('results'), list)
    assert isinstance(response.get('response').get('results'), list)
    assert response.get('request').get(
        f'ef-{first_key}') == test_cells[first_key]


def test_get_browse_results_for_item_ids_with_valid_item_ids_and_segments():
    '''Should return a response with a valid ids, section, and segments'''

    segments = ['foo', 'bar']
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results_for_item_ids(
        IDS,
        {},
        {'segments': segments})

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('results'), list)
    assert response.get('request').get('us') == segments


def test_get_browse_results_for_item_ids_with_valid_item_ids_and_user_id():
    '''Should return a response with a valid ids and user_id'''

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        browse = ConstructorIO({**VALID_OPTIONS, 'requests': requests}).browse
        response = browse.get_browse_results_for_item_ids(
            IDS,
            {},
            {'user_id': USER_ID})
        request_url = mocked_requests.call_args.args[0]

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert isinstance(response.get('response').get('results'), list)
        assert re.search('ui=user-id', request_url)


def test_get_browse_results_for_item_ids_with_valid_item_ids_and_page():
    '''Should return a response with a valid ids, section, and page'''

    page = 1
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results_for_item_ids(
        IDS,
        {'section': SECTION,'page': page})

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('results'), list)
    assert response.get('request').get('page') == page


def test_get_browse_results_for_item_ids_with_valid_item_ids_and_results_per_page():
    '''Should return a response with a valid ids, section, and results_per_page''' # pylint: disable=line-too-long

    results_per_page = 2
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results_for_item_ids(
        IDS,
        {'results_per_page': results_per_page}
    )
    num_results = response.get('request').get('num_results_per_page')

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('results'), list)
    assert num_results == results_per_page


def test_get_browse_results_for_item_ids_with_valid_item_ids_and_filters():
    '''Should return a response with a valid ids, section, and filters'''

    filters = {'keywords': ['battery-powered']}
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results_for_item_ids(
        IDS,
        {'section': SECTION, 'filters': filters})

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('results'), list)
    assert response.get('request').get('filters') == filters


def test_get_browse_results_for_item_ids_with_valid_item_ids_and_fmt_options():
    '''Should return a response with a valid ids, section, and fmt_options'''

    fmt_options = {'groups_max_depth': 2, 'groups_start': 'current'}
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results_for_item_ids(
        IDS,
        {'section': SECTION, 'fmt_options': fmt_options})

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('results'), list)
    assert response.get('request').get('fmt_options') == fmt_options


def test_get_browse_results_for_item_ids_with_valid_item_ids_and_sort_by():
    '''Should return a response with a valid ids, section, and sort_by'''

    sort_by = 'relevance'
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results_for_item_ids(
        IDS,
        {'section': SECTION, 'sort_by': sort_by})

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('results'), list)
    assert response.get('request').get('sort_by') == sort_by


def test_get_browse_results_for_item_ids_with_valid_item_ids_and_sort_order():
    '''Should return a response with a valid ids, section, and sort_by'''

    sort_order = 'ascending'
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results_for_item_ids(
        IDS,
        {'section': SECTION, 'sort_order': sort_order})

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('results'), list)
    assert response.get('request').get('sort_order') == sort_order


def test_get_browse_results_for_item_ids_with_valid_item_ids_and_user_ip():
    '''Should return a response with a valid ids, section, and user_ip'''

    user_ip = '127.0.0.1'

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        browse = ConstructorIO({**VALID_OPTIONS, 'requests': requests}).browse
        response = browse.get_browse_results_for_item_ids(
            IDS,
            {'section': SECTION},
            {'user_ip': user_ip})
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert isinstance(response.get('response').get('results'), list)
        assert headers.get('X-Forwarded-For') == user_ip


def test_get_browse_results_for_item_ids_with_valid_item_ids_and_security_token():
    '''Should return a response with a valid ids, section, and security_token''' # pylint: disable=line-too-long

    security_token = 'cio-python-test'

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        browse = ConstructorIO({
            **VALID_OPTIONS,
            'requests': requests,
            'security_token': security_token
        }).browse
        response = browse.get_browse_results_for_item_ids(
            IDS,
            {'section': SECTION})
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert isinstance(response.get('response').get('results'), list)
        assert headers.get('x-cnstrc-token') == security_token


def test_get_browse_results_for_item_ids_with_valid_item_ids_and_user_agent():
    '''Should return a response with a valid ids, section, and user_agent'''

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'  # pylint: disable=line-too-long

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        browse = ConstructorIO({**VALID_OPTIONS, 'requests': requests}).browse
        response = browse.get_browse_results_for_item_ids(
            IDS,
            {'section': SECTION},
            {'user_agent': user_agent}
        )
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert isinstance(response.get('response').get('results'), list)
        assert headers.get('User-Agent') == user_agent


def test_get_browse_results_for_item_ids_with_valid_item_ids_with_result_id():
    '''Should return a response with a valid ids, and section with a result_id appended to each result'''  # pylint: disable=line-too-long

    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results_for_item_ids(
        IDS,
        {'section': SECTION})

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('results'), list)
    assert isinstance(response.get('response').get('results'), list)

    for result in response.get('response').get('results'):
        assert isinstance(result.get('result_id'), str)
        assert result.get('result_id') == response.get('result_id')


def test_get_browse_results_for_item_ids_with_valid_item_ids_and_hidden_fields():
    '''Should return a response with a valid ids, section, and hiddenFields''' # pylint: disable=line-too-long

    hidden_fields = ['hidden_field1', 'hidden_field2']
    browse = ConstructorIO(VALID_OPTIONS).browse
    response = browse.get_browse_results_for_item_ids(
        IDS,
        {'section': SECTION, 'hidden_fields': hidden_fields}
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert isinstance(response.get('response').get('results'), list)
    assert response.get('request').get('hidden_fields') == hidden_fields


def test_get_browse_results_for_item_ids_with_invalid_item_ids():
    '''Should raise exception when invalid item_ids is provided'''

    with raises(Exception, match=r'item_ids is a required parameter of type list'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results_for_item_ids({})


def test_get_browse_results_for_item_ids_with_missing_item_ids():
    '''Should raise exception when item_ids is missing'''

    with raises(Exception, match=r"get_browse_results_for_item_ids\(\) missing 1 required positional argument: 'item_ids'"): # pylint: disable=line-too-long
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results_for_item_ids() # pylint: disable=no-value-for-parameter


def test_get_browse_results_for_item_ids_with_invalid_page():
    '''Should raise exception when invalid page parameter is provided'''

    with raises(Exception, match=r'page must be an integer'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results_for_item_ids(
            IDS,
            {'section': SECTION, 'page': 'abc'})


def test_get_browse_results_for_item_ids_with_invalid_results_per_page():
    '''Should raise exception when invalid results_per_page parameter is provided'''

    with raises(Exception, match=r'num_results_per_page must be an integer'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results_for_item_ids(
            IDS,
            {'section': SECTION, 'results_per_page': 'abc'})


def test_get_browse_results_for_item_ids_with_invalid_filters():
    '''Should raise exception when invalid filters parameter is provided'''

    with raises(Exception, match=r'filters must be a dictionary'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results_for_item_ids(
            IDS,
            {'section': SECTION, 'filters': 'abc'})


def test_get_browse_results_for_item_ids_with_invalid_sort_by():
    '''Should raise exception when invalid sort_by parameter is provided'''

    with raises(Exception, match=r'sort_by must be a string'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results_for_item_ids(
            IDS,
            {'section': SECTION, 'sort_by': ['foo', 'bar']})


def test_get_browse_results_for_item_ids_with_invalid_sort_order():
    '''Should raise exception when invalid sort_order parameter is provided'''

    with raises(Exception, match=r'Invalid value for parameter: "sort_order"'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results_for_item_ids(
            IDS,
            {'section': SECTION, 'sort_order': 123})


def test_get_browse_results_for_item_ids_with_invalid_section():
    '''Should raise exception when invalid section parameter is provided'''

    with raises(Exception, match=r'Unknown section: 123'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results_for_item_ids(
            IDS,
            {'section': 123})


def test_get_browse_results_for_item_ids_with_invalid_fmt_options():
    '''Should raise exception when invalid fmt_options parameter is provided'''

    with raises(Exception, match=r'fmt_options must be a dictionary'):
        browse = ConstructorIO(VALID_OPTIONS).browse
        browse.get_browse_results_for_item_ids(
            IDS,
            {'fmt_options': 'abc'})


def test_get_browse_results_for_item_ids_with_invalid_api_key():
    '''Should raise exception when invalid api_key is provided'''

    with raises(
            Exception,
            match=r'We have no record of this key. You can find your key at app.constructor.io/dashboard.'  # pylint: disable=line-too-long
    ):
        browse = ConstructorIO({
            **VALID_OPTIONS,
            'api_key': 'fyzs7tfF8L161VoAXQ8u'
        }).browse
        browse.get_browse_results_for_item_ids(
            IDS,
            {'section': SECTION})


def test_get_browse_results_for_item_ids_with_no_api_key():
    '''Should raise exception when no api_key is provided'''

    with raises(Exception, match=r'API key is a required parameter of type string'):
        browse = ConstructorIO({}).browse
        browse.get_browse_results_for_item_ids(IDS)
