'''ConstructorIO Python Client - Recommendation Page Tests'''

import json
from os import environ
from unittest import mock
from urllib.parse import parse_qs, unquote, urlparse

import requests
from pytest import mark, raises

from constructor_io.constructor_io import ConstructorIO
from constructor_io.helpers.exception import ConstructorException

MOCK_API_KEY = 'key_mock_page_api'
VALID_CLIENT_ID = '2b23dd74-5672-4379-878c-9182938d2710'
VALID_SESSION_ID = 2
PAGE_ID = 'pdp_b2c'
ITEM_ID = 'product-123'
PAGE_RESULT_ID = 'page-result-id'
PAGE_RESPONSE = {
    'request': {'page_id': PAGE_ID, 'item_id': ITEM_ID, 'num_results': 10},
    'response': {
        'page_id': PAGE_ID,
        'display_name': 'PDP - B2C',
        'page_type': 'pdp',
        'pods': [
            {
                'pod_id': 'similar_items',
                'request': {'item_id': ITEM_ID, 'num_results': 12},
                'response': {
                    'results': [
                        {'data': {'id': 'product-987'}, 'value': 'Red Running Shoe'},
                        {'data': {'id': 'product-988'}, 'value': 'Blue Running Shoe'},
                    ],
                    'total_num_results': 2,
                    'pod': {'id': 'similar_items', 'display_name': 'Similar Items'},
                },
                'result_id': 'similar-items-result-id',
            },
            {
                'pod_id': 'complete_the_look',
                'request': {'item_id': ITEM_ID, 'num_results': 8},
                'response': {
                    'results': [],
                    'total_num_results': 0,
                    'pod': {'id': 'complete_the_look', 'display_name': 'Complete the Look'},
                },
                'result_id': 'complete-the-look-result-id',
            },
        ],
    },
    'result_id': PAGE_RESULT_ID,
}


def mock_response(body):
    '''Build a successful mocked response returning a copy of body'''

    response = mock.MagicMock(ok=True)
    response.json.return_value = json.loads(json.dumps(body))
    return response


def request_url_of(mocked_get):
    '''Return the URL of the last mocked GET'''

    return mocked_get.call_args.args[0]


def query_of(mocked_get):
    '''Return the parsed query of the last mocked GET'''

    return parse_qs(urlparse(request_url_of(mocked_get)).query)


def test_requests_page_endpoint_with_shared_parameters():
    '''Should request the page endpoint with shared and user parameters'''

    recommendations = ConstructorIO({'api_key': MOCK_API_KEY, 'security_token': 'token'}).recommendations

    with mock.patch.object(requests, 'get', return_value=mock_response(PAGE_RESPONSE)) as mocked_get:
        recommendations.get_recommendation_page_results(
            PAGE_ID,
            {
                'item_ids': ITEM_ID,
                'num_results': 10,
                'section': 'Products',
                'filters': {'in_stock': 'true'},
                'filter_match_types': {'color': 'any'},
            },
            {
                'client_id': VALID_CLIENT_ID,
                'session_id': VALID_SESSION_ID,
                'user_id': 'user-id',
                'segments': ['vip'],
                'user_ip': '127.0.0.1',
            },
        )

    query = query_of(mocked_get)
    headers = mocked_get.call_args.kwargs.get('headers')

    assert urlparse(request_url_of(mocked_get)).path == f'/recommendations/v1/pages/{PAGE_ID}'
    assert query['key'] == [MOCK_API_KEY]
    assert query['i'] == [VALID_CLIENT_ID]
    assert query['s'] == [str(VALID_SESSION_ID)]
    assert query['ui'] == ['user-id']
    assert query['us'] == ['vip']
    assert '_dt' in query
    assert query['item_id'] == [ITEM_ID]
    assert query['num_results'] == ['10']
    assert query['section'] == ['Products']
    assert query['filters[in_stock]'] == ['true']
    assert query['filter_match_types[color]'] == ['any']
    assert not [key for key in query if key.startswith('pod_overrides')]
    assert headers['x-cnstrc-token'] == 'token'
    assert headers['X-Forwarded-For'] == '127.0.0.1'


def test_encodes_pod_overrides_in_bracket_notation():
    '''Should encode pod_overrides in bracket notation with the same wire format as shared parameters'''

    recommendations = ConstructorIO({'api_key': MOCK_API_KEY}).recommendations
    pre_filter_expression = {'or': [{'name': 'brand', 'value': 'acme'}]}
    variations_map = {'group_by': [{'name': 'color', 'field': 'data.color'}], 'values': {}, 'dtype': 'array'}

    with mock.patch.object(requests, 'get', return_value=mock_response(PAGE_RESPONSE)) as mocked_get:
        recommendations.get_recommendation_page_results(
            PAGE_ID,
            {
                'item_ids': ITEM_ID,
                'num_results': 10,
                'pod_overrides': {
                    'similar_items': {'num_results': 0},
                    'complete_the_look': {
                        'num_results': 8,
                        'filters': {'in_stock': 'true', 'color': ['red', 'blue']},
                        'filter_match_types': {'color': 'all'},
                        'pre_filter_expression': pre_filter_expression,
                        'variations_map': variations_map,
                        'fmt_options': {'groups_max_depth': 2},
                        'hidden_fields': ['inventory', 'margin'],
                    },
                },
            },
        )

    query = query_of(mocked_get)
    prefix = 'pod_overrides[complete_the_look]'

    assert 'pod_overrides[similar_items][num_results]=0' in unquote(request_url_of(mocked_get))
    assert query['num_results'] == ['10']
    assert query[f'{prefix}[num_results]'] == ['8']
    assert query[f'{prefix}[filters][in_stock]'] == ['true']
    assert query[f'{prefix}[filters][color]'] == ['red', 'blue']
    assert query[f'{prefix}[filter_match_types][color]'] == ['all']
    assert json.loads(query[f'{prefix}[pre_filter_expression]'][0]) == pre_filter_expression
    assert json.loads(query[f'{prefix}[variations_map]'][0]) == variations_map
    assert query[f'{prefix}[fmt_options][groups_max_depth]'] == ['2']
    assert query[f'{prefix}[fmt_options][hidden_fields]'] == ['inventory', 'margin']


def test_stamps_each_pod_result_id_onto_its_results():
    '''Should stamp each pod's own result_id onto its results, not the page result_id'''

    recommendations = ConstructorIO({'api_key': MOCK_API_KEY}).recommendations

    with mock.patch.object(requests, 'get', return_value=mock_response(PAGE_RESPONSE)):
        response = recommendations.get_recommendation_page_results(PAGE_ID, {'item_ids': ITEM_ID})

    similar_items, complete_the_look = response['response']['pods']

    assert response['result_id'] == PAGE_RESULT_ID
    assert [result['result_id'] for result in similar_items['response']['results']] == [
        'similar-items-result-id',
        'similar-items-result-id',
    ]
    assert complete_the_look['response']['results'] == []


def test_raises_when_response_has_no_pods():
    '''Should raise when the response has no pods'''

    recommendations = ConstructorIO({'api_key': MOCK_API_KEY}).recommendations

    with mock.patch.object(requests, 'get', return_value=mock_response({'response': {}})):
        with raises(ConstructorException, match='get_recommendation_page_results response data is malformed'):
            recommendations.get_recommendation_page_results(PAGE_ID)


def test_raises_when_page_id_is_missing():
    '''Should raise when page_id is not provided'''

    recommendations = ConstructorIO({'api_key': MOCK_API_KEY}).recommendations

    with raises(ConstructorException, match='page_id is a required parameter of type string'):
        recommendations.get_recommendation_page_results(None)


def test_raises_when_pod_overrides_contain_page_wide_parameter():
    '''Should raise when pod_overrides contains a page-wide parameter'''

    recommendations = ConstructorIO({'api_key': MOCK_API_KEY}).recommendations

    with raises(ConstructorException, match='cannot be overridden per pod: item_ids'):
        recommendations.get_recommendation_page_results(
            PAGE_ID,
            {'pod_overrides': {'similar_items': {'item_ids': 'other'}}},
        )


def test_raises_when_variation_id_is_provided_without_item_ids():
    '''Should raise when variation_id is provided without item_ids'''

    recommendations = ConstructorIO({'api_key': MOCK_API_KEY}).recommendations

    with raises(ConstructorException, match='item_ids is a required parameter for variation_id'):
        recommendations.get_recommendation_page_results(PAGE_ID, {'variation_id': 'v1'})


# The page endpoint is not yet enabled on the test index, and the test index has no
# page configured (`/recommendations/v1/pages/pdp_b2c` returns 404 there)
@mark.skip(reason='the page endpoint is not enabled and no page is configured on the test index')
def test_live_page_results_use_per_pod_result_ids():
    '''Should return each pod's own result_id on its results'''

    recommendations = ConstructorIO({'api_key': environ.get('TEST_REQUEST_API_KEY')}).recommendations
    response = recommendations.get_recommendation_page_results(PAGE_ID, {'item_ids': 'power_drill'})

    assert isinstance(response.get('result_id'), str)
    assert response['response']['pods']
    for pod in response['response']['pods']:
        assert pod['result_id'] != response['result_id']
        assert pod['response']['pod']['id'] == pod['pod_id']
        for result in pod['response']['results']:
            assert result['result_id'] == pod['result_id']
