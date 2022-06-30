'''Utility functions'''

import json
from re import sub
from urllib.parse import parse_qs, quote, unquote

from constructor_io.helpers.exception import (ConstructorException,
                                              HttpException)


def throw_http_exception_from_response(response):
    '''Throw custom HTTP exception from an API response'''

    response_json = response.json()
    exception = HttpException(
        response_json.get('message'),
        response_json.get('status'),
        response_json.get('status_text'),
        response_json.get('url'),
        response_json.get('headers'),
    )

    raise exception

def create_auth_header(options):
    '''Create Basic Auth header'''

    return (options.get('api_token'),'')

def clean_params(params_obj):
    '''Clean query parameters'''

    cleaned_params = {}

    for key, value in params_obj.items():
        if isinstance(value, str):
            # Replace non-breaking spaces (or any other type of spaces caught by the regex)
            # - with a regular white space
            cleaned_params[key] = unquote(our_encode_uri_component(value))
        elif value is not None:
            cleaned_params[key] = value

    return cleaned_params

def our_encode_uri_component(string):
    '''Replace special characters'''

    if string:
        str_replaced = sub('&', '%26', string)
        parsed_str_obj = parse_qs(f's={str_replaced}')
        decoded = sub(r'\s', ' ', parsed_str_obj['s'][0])

        return quote(decoded)

    return None

def create_shared_query_params(options, parameters, user_parameters):
    # pylint: disable=too-many-branches
    '''Create query params shared between modules'''

    query_params = {
        'c': options.get('version'),
        'key': options.get('api_key'),
        'i': user_parameters.get('client_id'),
        's': user_parameters.get('session_id'),
    }

    if parameters:
        if parameters.get('page'):
            query_params['page'] = parameters.get('page')

        if parameters.get('results_per_page'):
            query_params['num_results_per_page'] = parameters.get('results_per_page')

        if parameters.get('filters'):
            filters = parameters.get('filters')
            if isinstance(filters, dict):
                for key, value in filters.items():
                    query_params[f'filters[{key}]'] = value
            else:
                raise ConstructorException('filters must be a dictionary')

        if parameters.get('sort_by'):
            query_params['sort_by'] = parameters.get('sort_by')

        if parameters.get('sort_order'):
            query_params['sort_order'] = parameters.get('sort_order')

        if parameters.get('section'):
            query_params['section'] = parameters.get('section')

        if parameters.get('hidden_fields'):
            query_params['fmt_options[hidden_fields]'] = parameters.get('hidden_fields')

        if parameters.get('hidden_facets'):
            query_params['fmt_options[hidden_facets]'] = parameters.get('hidden_facets')

        if parameters.get('fmt_options'):
            fmt_options = parameters.get('fmt_options')
            if isinstance(fmt_options, dict):
                for key, value in fmt_options.items():
                    query_params[f'fmt_options[{key}]'] = value
            else:
                raise ConstructorException('fmt_options must be a dictionary')

        if parameters.get('variations_map'):
            query_params['variations_map'] = json.dumps(parameters.get('variations_map'))

    if user_parameters.get('test_cells'):
        for key, value in user_parameters.get('test_cells').items():
            query_params[f'ef-{key}'] = value

    if user_parameters.get('segments') and len(user_parameters.get('segments')):
        query_params['us'] = user_parameters.get('segments')

    if user_parameters.get('user_id'):
        query_params['ui'] = user_parameters.get('user_id')

    return query_params

def create_request_headers(options, user_parameters=None):
    '''Create request headers shared between modules'''

    if not user_parameters:
        user_parameters = {}

    headers = {}
    security_token = options.get('security_token')
    user_ip = user_parameters.get('user_ip')
    user_agent = user_parameters.get('user_agent')

    # Append security token as 'x-cnstrc-token' if available
    if security_token and isinstance(security_token, str):
        headers['x-cnstrc-token'] = security_token

    # Append user IP as 'X-Forwarded-For' if available
    if user_ip and isinstance(user_ip, str):
        headers['X-Forwarded-For'] = user_ip

    # Append user agent as 'User-Agent' if available
    if user_agent and isinstance(user_agent, str):
        headers['User-Agent'] = user_agent

    return headers
