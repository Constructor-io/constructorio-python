'''Utility functions'''

from re import sub
from urllib.parse import parse_qs, urlencode

from constructorio_python.helpers.exception import HttpException


def throw_http_exception_from_response(response):
    '''Throw custom HTTP exception from an API response'''

    json = response.json()
    exception = HttpException(
        json.get('message'),
        json.get('status'),
        json.get('status_text'),
        json.get('url'),
        json.get('headers'),
    )

    raise exception

def create_auth_header(options):
    '''Create Basic Auth header'''

    return (options.get('api_token'),'')

def clean_params(params_obj):
    cleaned_params = {}

    for key, value in params_obj.items():
        if isinstance(value, str):
            # Replace non-breaking spaces (or any other type of spaces caught by the regex)
            # - with a regular white space
            cleaned_params[key] = our_encode_uri_component(value)
        else:
            cleaned_params[key] = value

    return cleaned_params

def our_encode_uri_component(string):
    if string:
        str_replaced = sub('&', '%26', string)
        parsed_str_obj = parse_qs(f's={str_replaced}')
        decoded = {
            "s": sub(r'\s', ' ', parsed_str_obj['s'][0])
        }

        return urlencode(decoded).split('=')[1];

    return None


