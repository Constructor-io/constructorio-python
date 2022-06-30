'''ConstructorIO Python Client - Recommendations Tests'''

import re
from os import environ
from unittest import mock

import requests
from pytest import raises

from constructor_io.constructor_io import ConstructorIO
from constructor_io.helpers.exception import (ConstructorException,
                                              HttpException)

TEST_API_KEY = environ['TEST_API_KEY']
VALID_CLIENT_ID = '2b23dd74-5672-4379-878c-9182938d2710'
VALID_SESSION_ID = 2
VALID_OPTIONS = { 'api_key': TEST_API_KEY }
POD_ID = 'home_page_1'
POD_ID_ALTERNATIVE_RECOMMENDATIONS = 'item_page_1'
POD_ID_QUERY_RECOMMENDATIONS = 'query_recommendations'
POD_ID_FILTERED_ITEMS_RECOMMENDATIONS = 'filtered_items'
ITEM_ID = 'power_drill'
ITEM_IDS = [ITEM_ID, 'drill']
TERM = 'apple'
SECTION = 'Products'
CLIENT_SESSION_IDENTIFIERS = {
    'client_id': VALID_CLIENT_ID,
    'session_id': VALID_SESSION_ID,
}

def test_with_valid_pod_id_and_identifiers():
    '''Should return a response with a valid pod_id and client + session identifiers'''

    recommendations = ConstructorIO(VALID_OPTIONS).recommendations
    response = recommendations.get_recommendation_results(
        POD_ID,
        {
            'section': SECTION,
        },
        CLIENT_SESSION_IDENTIFIERS,
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('pod_id') == POD_ID

def test_with_valid_pod_id_and_test_cells():
    '''Should return a response with a valid pod_id and test_cells'''

    test_cells = { 'foo': 'bar' }
    recommendations = ConstructorIO(VALID_OPTIONS).recommendations
    response = recommendations.get_recommendation_results(
        POD_ID,
        {},
        {
            **CLIENT_SESSION_IDENTIFIERS,
            'test_cells': test_cells,
        }
    )
    first_key = next(iter(test_cells.keys()))

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get(f'ef-{first_key}') == test_cells[first_key]

def test_with_valid_pod_id_and_segments():
    '''Should return a response with a valid pod_id and segments'''

    segments = ['foo', 'bar']
    recommendations = ConstructorIO(VALID_OPTIONS).recommendations
    response = recommendations.get_recommendation_results(
        POD_ID,
        {},
        {
            **CLIENT_SESSION_IDENTIFIERS,
            'segments': segments,
        },
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('us') == segments

def test_with_valid_pod_id_and_user_id():
    '''Should return a response with a valid pod_id and user_id'''

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        user_id = 'user-id'
        recommendations = ConstructorIO({ **VALID_OPTIONS, 'requests': requests }).recommendations
        response = recommendations.get_recommendation_results(
            POD_ID,
            {},
            {
                **CLIENT_SESSION_IDENTIFIERS,
                'user_id': user_id,
            },
        )
        request_url = mocked_requests.call_args.args[0]

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert re.search('ui=user-id', request_url)

def test_with_valid_pod_id_and_num_results():
    '''Should return a response with a valid pod_id and num_results'''

    num_results = 4
    recommendations = ConstructorIO(VALID_OPTIONS).recommendations
    response = recommendations.get_recommendation_results(
        POD_ID,
        { 'num_results': num_results },
        { **CLIENT_SESSION_IDENTIFIERS },
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('num_results') == num_results


def test_with_valid_pod_id_and_user_ip():
    '''Should return a response with a valid pod_id and user_ip'''

    user_ip = '127.0.0.1'

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        recommendations = ConstructorIO({ **VALID_OPTIONS, 'requests': requests }).recommendations
        response = recommendations.get_recommendation_results(
            POD_ID,
            {},
            { **CLIENT_SESSION_IDENTIFIERS, 'user_ip': user_ip }
        )
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert headers.get('X-Forwarded-For') == user_ip

def test_with_valid_pod_id_and_security_token():
    '''Should return a response with a valid pod_id and security_token'''

    security_token = 'cio-python-test'

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        recommendations = ConstructorIO({
            **VALID_OPTIONS,
            'requests': requests,
            'security_token': security_token
        }).recommendations
        response = recommendations.get_recommendation_results(
          POD_ID,
          {},
          { **CLIENT_SESSION_IDENTIFIERS }
        )
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert headers.get('x-cnstrc-token') == security_token

def test_with_valid_pod_id_and_user_agent():
    '''Should return a response with a valid pod_id and user_agent'''

    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36' # pylint: disable=line-too-long

    with mock.patch.object(requests, 'get', wraps=requests.get) as mocked_requests:
        recommendations = ConstructorIO({ **VALID_OPTIONS, 'requests': requests }).recommendations
        response = recommendations.get_recommendation_results(
          POD_ID,
          {},
          {
              **CLIENT_SESSION_IDENTIFIERS,
              'user_agent': user_agent,
          },
        )
        headers = mocked_requests.call_args.kwargs.get('headers')

        assert isinstance(response.get('request'), dict)
        assert isinstance(response.get('response'), dict)
        assert isinstance(response.get('result_id'), str)
        assert headers.get('User-Agent') == user_agent

def test_with_valid_pod_id_with_result_id():
    '''Should return a response with a valid pod_id with a result_id appended to each result'''

    recommendations = ConstructorIO(VALID_OPTIONS).recommendations
    response = recommendations.get_recommendation_results(
        POD_ID,
        {},
        { **CLIENT_SESSION_IDENTIFIERS },
    )
    results = response.get('response').get('results')

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)

    for result in results:
        assert isinstance(result.get('result_id'), str)
        assert result.get('result_id') == response.get('result_id')

def test_with_valid_pod_id_and_item_ids_singular():
    '''Should return a response with a valid pod_id and item_ids (singular)'''

    recommendations = ConstructorIO(VALID_OPTIONS).recommendations
    response = recommendations.get_recommendation_results(
        POD_ID,
        { 'item_ids': ITEM_ID, },
        { **CLIENT_SESSION_IDENTIFIERS },
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('item_id') == ITEM_ID

def test_with_valid_pod_id_and_item_ids_multiple():
    '''Should return a response with a valid pod_id and item_ids (multiple)'''

    recommendations = ConstructorIO(VALID_OPTIONS).recommendations
    response = recommendations.get_recommendation_results(
        POD_ID,
        { 'item_ids': ITEM_IDS },
        { **CLIENT_SESSION_IDENTIFIERS },
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('item_id') == ITEM_IDS

def test_with_valid_pod_id_and_term():
    '''Should return a response with a valid term for query recommendations strategy pod'''

    recommendations = ConstructorIO(VALID_OPTIONS).recommendations
    response = recommendations.get_recommendation_results(
        POD_ID_QUERY_RECOMMENDATIONS,
        { 'term': TERM },
        { **CLIENT_SESSION_IDENTIFIERS },
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('term') == TERM

def test_with_valid_pod_id_and_filters():
    '''Should return a response with a valid filter for filtered items strategy pod'''

    filters = { 'keywords': ['battery-powered'] }
    recommendations = ConstructorIO(VALID_OPTIONS).recommendations
    response = recommendations.get_recommendation_results(
        POD_ID_FILTERED_ITEMS_RECOMMENDATIONS,
        { 'filters': filters },
        { **CLIENT_SESSION_IDENTIFIERS },
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('filters').get('keywords') == filters['keywords'][0]

def test_with_valid_pod_id_and_multiple_filters():
    '''Should return a response with valid filters for filtered items strategy pod'''

    filters = { 'group_id': ['All'], 'Brand': ['XYZ', 'ABC'] }
    recommendations = ConstructorIO(VALID_OPTIONS).recommendations
    response = recommendations.get_recommendation_results(
        POD_ID_FILTERED_ITEMS_RECOMMENDATIONS,
        { 'filters': filters },
        { **CLIENT_SESSION_IDENTIFIERS },
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('filters').get('group_id') == filters['group_id'][0]
    assert response.get('request').get('filters').get('Brand') == filters['Brand']

def test_with_valid_pod_id_and_variations_map():
    '''Should return a response with a variations map'''

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
    filters = { 'keywords': ['battery-powered'] }
    recommendations = ConstructorIO(VALID_OPTIONS).recommendations
    response = recommendations.get_recommendation_results(
        POD_ID_FILTERED_ITEMS_RECOMMENDATIONS,
        { 'filters': filters, 'variations_map': variations_map },
        { **CLIENT_SESSION_IDENTIFIERS },
    )

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('filters').get('keywords') == filters['keywords'][0]
    assert response.get('request').get('variations_map') == variations_map

def test_with_invalid_api_key():
    '''Should raise exception when invalid api_key is provided'''

    with raises(
            HttpException,
            match=r'We have no record of this key. You can find your key at app.constructor.io/dashboard.' # pylint: disable=line-too-long
    ):
        recommendations = ConstructorIO({
            **VALID_OPTIONS,
            'api_key': 'fyzs7tfF8L161VoAXQ8u'
        }).recommendations
        recommendations.get_recommendation_results(POD_ID)

def test_with_no_api_key():
    '''Should raise exception when no api_key is provided'''

    with raises(ConstructorException, match=r'API key is a required parameter of type string'):
        recommendations = ConstructorIO({}).recommendations
        recommendations.get_recommendation_results(POD_ID)

def test_with_invalid_pod_id():
    '''Should raise exception when invalid pod_id is provided'''

    with raises(ConstructorException, match=r'pod_id is a required parameter of type string'):
        recommendations = ConstructorIO(VALID_OPTIONS).recommendations
        recommendations.get_recommendation_results(
            [],
            {},
            { **CLIENT_SESSION_IDENTIFIERS },
        )

def test_with_no_pod_id():
    '''Should raise exception when no pod_id is provided'''

    with raises(ConstructorException, match=r'pod_id is a required parameter of type string'):
        recommendations = ConstructorIO(VALID_OPTIONS).recommendations
        recommendations.get_recommendation_results(
            None,
            {},
            { **CLIENT_SESSION_IDENTIFIERS },
        )

def test_with_invalid_num_results():
    '''Should raise exception when invalid num_results is provided'''

    with raises(ConstructorException, match=r'num_results must be an integer'):
        recommendations = ConstructorIO(VALID_OPTIONS).recommendations
        recommendations.get_recommendation_results(
            POD_ID,
            { 'num_results': 'abc' },
            { **CLIENT_SESSION_IDENTIFIERS },
        )

def test_with_invalid_filters():
    '''Should raise exception when invalid filters is provided'''

    with raises(ConstructorException, match=r'filters must be a dictionary'):
        recommendations = ConstructorIO(VALID_OPTIONS).recommendations
        recommendations.get_recommendation_results(
            POD_ID_FILTERED_ITEMS_RECOMMENDATIONS,
            { 'filters': 'abc' },
            { **CLIENT_SESSION_IDENTIFIERS },
        )

def test_with_invalid_item_ids():
    '''Should raise exception when invalid item_ids is provided'''

    with raises(ConstructorException, match=r'item_id is a required field of type string'):
        recommendations = ConstructorIO(VALID_OPTIONS).recommendations
        recommendations.get_recommendation_results(
            POD_ID_ALTERNATIVE_RECOMMENDATIONS,
            { 'item_ids': {} },
            { **CLIENT_SESSION_IDENTIFIERS },
        )
