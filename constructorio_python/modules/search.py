'''Search Module'''

from time import time
from urllib.parse import quote, urlencode

import requests as r

from constructorio_python.helpers.utils import (
    clean_params, create_auth_header, throw_http_exception_from_response)


def create_search_url(query, parameters, user_parameters, options):
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
                raise Exception('filters must be a dictionary')

        if parameters.get('sort_by'):
            query_params['sort_by'] = parameters.get('sort_by')

        if parameters.get('sort_order'):
            query_params['sort_order'] = parameters.get('sort_order')

        if parameters.get('section'):
            query_params['section'] = parameters.get('section')

        if parameters.get('fmt_options'):
            fmt_options = parameters.get('fmt_options')
            if isinstance(fmt_options, dict):
                for key, value in fmt_options.items():
                    query_params[f'fmt_options[{key}]'] = value
            else:
                raise Exception('fmt_options must be a dictionary')

        if parameters.get('hidden_fields'):
            query_params['hidden_fields'] = parameters.get('hidden_fields')

    query_params['_dt'] = int(time()*1000.0)
    query_params = clean_params(query_params)
    query_string = urlencode(query_params, doseq=True)

    return f'{options.get("service_url")}/search/{quote(query)}?{query_string}'

class Search:
    # pylint: disable=too-few-public-methods
    '''Search Class'''

    def __init__(self, options) -> None:
        self.__options = options or {}

    def get_search_results(self, query, parameters=None, user_parameters=None):
        '''
        Retrieve search results from API

        :param str query: Search query
        :param dict parameters: Additional parameters to refine result set
        :param int parameters.page: The page number of the results
        :param int parameters.results_per_page: The number of results per page to return
        :param dict parameters.filters: Filters used to refine search
        :param str parameters.sort_by: The sort method for results
        :param str parameters.sort_order: The sort order for results
        :param str parameters.section: Section name for results
        :param dict parameters.fmt_options: The format options used to refine result groups
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
        request_url = create_search_url(query, parameters, user_parameters, self.__options)
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
        json_response = json.get('response')

        if json_response:
            if json_response.get('results') or json_response.get('results') == []:
                result_id = json.get('result_id')
                if result_id:
                    for result in json_response.get('results'):
                        result['result_id'] = result_id

                return json

            # Redirect rules
            if json_response.get('redirect'):
                return json

        raise Exception('get_search_results response data is malformed')
