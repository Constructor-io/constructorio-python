'''ConstructorIO Python Client - Tracker Tests'''

from unittest import mock
from urllib.parse import parse_qs, urlparse

from pytest import raises

from constructor_io.constructor_io import ConstructorIO
from constructor_io.helpers.exception import (ConstructorException,
                                              HttpException)

VALID_CLIENT_ID = '2b23dd74-5672-4379-878c-9182938d2710'
VALID_SESSION_ID = 2
VALID_OPTIONS = { 'api_key': 'test-api-key' }
USER_PARAMETERS = { 'client_id': VALID_CLIENT_ID, 'session_id': VALID_SESSION_ID }
TERM = 'item'
RESULT_ID = 'a1b2c3d4-result-id'

def _track(parameters=None, user_parameters=None, options=None, ok=True):
    mocked_requests = mock.Mock()
    mocked_requests.post.return_value.ok = ok
    mocked_requests.post.return_value.json.return_value = { 'message': 'Bad request', 'status': 400 }
    tracker = ConstructorIO({ **VALID_OPTIONS, **(options or {}), 'requests': mocked_requests }).tracker
    response = tracker.track_search_results_loaded(TERM, parameters, user_parameters or USER_PARAMETERS)
    call = mocked_requests.post.call_args

    return response, call

def test_with_valid_term_and_identifiers():
    '''Should send a POST to search_result_load with the shared query params'''

    response, call = _track({ 'result_count': 10 })
    url = urlparse(call.args[0])
    query = parse_qs(url.query)

    assert response is True
    assert url.path == '/v2/behavioral_action/search_result_load'
    assert query['key'] == ['test-api-key']
    assert query['i'] == [VALID_CLIENT_ID]
    assert query['s'] == [str(VALID_SESSION_ID)]
    assert query['c'][0].startswith('ciopython-')
    assert query['beacon'] == ['true']
    assert query['_dt'][0].isdigit()

def test_with_result_id_and_items():
    '''Should send result_id, items and the other fields in the body'''

    _, call = _track({
        'result_count': 167,
        'result_id': RESULT_ID,
        'items': ['KMH876', { 'item_id': 'KMH140', 'variation_id': 'KMH140-1' }],
        'result_page': 2,
        'section': 'Products',
        'url': 'https://example.com/search?q=item',
    })
    body = call.kwargs.get('json')

    assert body['search_term'] == TERM
    assert body['result_count'] == 167
    assert body['result_id'] == RESULT_ID
    assert body['items'] == [
        { 'item_id': 'KMH876' },
        { 'item_id': 'KMH140', 'variation_id': 'KMH140-1' },
    ]
    assert body['result_page'] == 2
    assert body['section'] == 'Products'
    assert body['url'] == 'https://example.com/search?q=item'

def test_without_result_id():
    '''Should leave result_id out of the body and default url and result_count'''

    _, call = _track({ 'items': ['a', 'b'] })
    body = call.kwargs.get('json')

    assert 'result_id' not in body
    assert body['url'] == 'N/A'
    assert body['result_count'] == 2

def test_with_more_than_100_items():
    '''Should send at most 100 items'''

    _, call = _track({ 'items': [str(i) for i in range(150)] })

    assert len(call.kwargs.get('json')['items']) == 100

def test_with_user_id_segments_and_headers():
    '''Should send user_id, segments, security token, user ip and user agent'''

    _, call = _track(
        { 'result_id': RESULT_ID },
        { **USER_PARAMETERS, 'user_id': 'user-id', 'segments': ['foo', 'bar'],
          'user_ip': '127.0.0.1', 'user_agent': 'test-agent' },
        { 'security_token': 'token' },
    )
    query = parse_qs(urlparse(call.args[0]).query)
    headers = call.kwargs.get('headers')

    assert query['ui'] == ['user-id']
    assert query['us'] == ['foo', 'bar']
    assert headers['x-cnstrc-token'] == 'token'
    assert headers['X-Forwarded-For'] == '127.0.0.1'
    assert headers['User-Agent'] == 'test-agent'

def test_with_invalid_term():
    '''Should raise exception when term is missing'''

    with raises(ConstructorException, match=r'term is a required parameter of type string'):
        ConstructorIO(VALID_OPTIONS).tracker.track_search_results_loaded(None, {}, USER_PARAMETERS)

def test_without_client_id():
    '''Should raise exception when client_id is missing'''

    with raises(ConstructorException, match=r'client_id is a required user parameter of type string'):
        _track({}, { 'session_id': VALID_SESSION_ID })

def test_without_session_id():
    '''Should raise exception when session_id is missing'''

    with raises(ConstructorException, match=r'session_id is a required user parameter of type int'):
        _track({}, { 'client_id': VALID_CLIENT_ID })

def test_with_error_response():
    '''Should raise HttpException when the API returns an error'''

    with raises(HttpException, match=r'Bad request'):
        _track({}, USER_PARAMETERS, ok=False)
