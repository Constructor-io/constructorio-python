'''ConstructorIO Python Client Tests'''

from os import environ

import pytest

from constructorio_python.constructorio import ConstructorIO
from constructorio_python.helpers.exception import ConstructorException

TEST_API_KEY = environ['TEST_API_KEY']
VALID_OPTIONS = { 'api_key': TEST_API_KEY }

def test_with_valid_api_key():
    '''Should return an instance when valid API key is provided'''

    client = ConstructorIO(VALID_OPTIONS)
    options = client.get_options()

    assert isinstance(client, ConstructorIO)
    assert options.get('api_key') == TEST_API_KEY
    assert options.get('version') is not None
    assert options.get('service_url') is not None
    assert client.autocomplete is not None
    assert client.search is not None
    assert client.browse is not None
    assert client.recommendations is not None

def test_with_valid_api_key_and_options():
    '''Should return an instance with custom options when valid API key is provided'''

    service_url = 'http://constructor.io'
    version = 'custom-version'
    api_token = 'token'
    security_token = 'security-token'
    client = ConstructorIO({
        **VALID_OPTIONS,
        'service_url': service_url,
        'version': version,
        'api_token': api_token,
        'security_token': security_token,
    })
    options = client.get_options()

    assert isinstance(client, ConstructorIO)
    assert options.get('api_key') == TEST_API_KEY
    assert options.get('version') == version
    assert options.get('service_url') == service_url
    assert options.get('api_token') == api_token
    assert options.get('security_token') == security_token

def test_with_invalid_api_key():
    '''Should throw an error when invalid API key is provided'''

    with pytest.raises(ConstructorException, match=r'API key is a required parameter of type string'):
        ConstructorIO({'api_key': 123456})

def test_with_no_api_key():
    '''Should throw an error when no API key is provided'''

    with pytest.raises(ConstructorException, match=r'API key is a required parameter of type string'):
        ConstructorIO({'api_key': None})

