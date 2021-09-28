'''Autocomplete Module'''

from time import time
from urllib.parse import quote, urlencode

import requests as r

from constructorio_python.helpers.utils import (
    clean_params, create_auth_header, throw_http_exception_from_response)


def create_autocomplete_url(query, parameters, user_parameters, options):
    # pylint: disable=too-many-branches
    '''Create URL from supplied query (term) and parameters'''

    query_params = {
        'c': options.get('version'),
        'key': options.get('api_key'),
        'i': user_parameters.get('client_id'),
        's': user_parameters.get('session_id'),
    }

    if not query or not isinstance(query, str):
        raise Exception('query is a required parameter of type string')

    if user_parameters.get('test_cells'):
        for key, value in user_parameters.get('test_cells').items():
            query_params[f'ef-{key}'] = value

    if user_parameters.get('segments') and len(user_parameters.get('segments')):
        query_params['us'] = user_parameters.get('segments')

    if user_parameters.get('user_id'):
        query_params['ui'] = user_parameters.get('user_id')

    if parameters:
        if parameters.get('num_results'):
            query_params['num_results'] = parameters.get('num_results')

        if parameters.get('results_per_section'):
            for key, value in parameters.get('results_per_section').items():
                query_params[f'num_results_{key}'] = value

        if parameters.get('filters'):
            filters = parameters.get('filters')
            if isinstance(filters, dict):
                for key, value in filters.items():
                    query_params[f'filters[{key}]'] = value
            else:
                raise Exception('filters must be a dictionary')

        if parameters.get('hidden_fields'):
            query_params['hidden_fields'] = parameters.get('hidden_fields')

    query_params['_dt'] = int(time()*1000.0)
    query_params = clean_params(query_params)
    query_string = urlencode(query_params, doseq=True)

    return f'{options.get("service_url")}/autocomplete/{quote(query)}?{query_string}'

class Autocomplete:
    # pylint: disable=too-few-public-methods
    '''Autocomplete Class'''

    def __init__(self, options):
        self.__options = options or {}

    def get_autocomplete_results(self, query, parameters=None, user_parameters=None):
        '''
        Retrieve autocomplete results from API

        :param str query: Autocomplete query
        :param dict parameters: Additional parameters to refine result set
        :param int parameters.num_results: The total number of results to return
        :param dict parameters.filters: Filters used to refine search
        :param int parameters.results_per_section: Number of results to return per section
        :param list parameters.hidden_fields: Hidden metadata fields to return
        :param dict user_parameters: Parameters relevant to the user request
        :param int user_parameters.session_id: Session ID, utilized to personalize results
        :param str user_parameters.client_id: Client ID, utilized to personalize results
        :param str user_parameters.user_id: User ID, utilized to personalize results
        :param str user_parameters.segments: User segments
        :param dict user_parameters.test_cells: User test cells
        :param str user_parameters.user_ip: Origin user IP, from client
        :param str user_parameters.user_agent: Origin user agent, from client

        :return: dict
        '''

        if not parameters:
            parameters = {}
        if not user_parameters:
            user_parameters = {}

        headers = {}
        request_url = create_autocomplete_url(query, parameters, user_parameters, self.__options)
        security_token = self.__options.get('security_token')
        user_ip = user_parameters.get('user_ip')
        user_agent = user_parameters.get('user_agent')
        requests = self.__options.get('requests') or r

        # Append security token as 'x-cnstrc-token' if available
        if security_token and isinstance(security_token, str):
            headers['x-cnstrc-token'] = security_token

        # Append user IP as 'X-Forwarded-For' if available
        if user_ip and isinstance(user_ip, str):
            headers['X-Forwarded-For'] = user_ip

        # Append user agent as 'User-Agent' if available
        if user_agent and isinstance(user_agent, str):
            headers['User-Agent'] = user_agent

        response = requests.get(
            request_url,
            auth=create_auth_header(self.__options),
            headers=headers
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        if json.get('sections'):
            if json.get('result_id'):
                for section_items in json.get('sections').values():
                    for item in section_items:
                        item['result_id'] = json.get('result_id')

            return json

        raise Exception('get_autocomplete_results response data is malformed')
