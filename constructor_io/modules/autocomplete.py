'''Autocomplete Module'''

from time import time
from urllib.parse import quote, urlencode

import requests as r

from constructor_io.helpers.exception import ConstructorException
from constructor_io.helpers.utils import (clean_params, create_auth_header,
                                          create_request_headers,
                                          create_shared_query_params,
                                          throw_http_exception_from_response)


def _create_autocomplete_url(query, parameters, user_parameters, options):
    # pylint: disable=too-many-branches
    '''Create URL from supplied query (term) and parameters'''

    query_params = create_shared_query_params(options, parameters, user_parameters)

    if not query or not isinstance(query, str):
        raise ConstructorException('query is a required parameter of type string')

    if parameters:
        if parameters.get('num_results'):
            query_params['num_results'] = parameters.get('num_results')

        if parameters.get('results_per_section'):
            for key, value in parameters.get('results_per_section').items():
                query_params[f'num_results_{key}'] = value

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
        :param dict parameters.results_per_section: Number of results to return per section
        :param list parameters.hidden_fields: Hidden metadata fields to return
        :param dict parameters.variations_map: The variations map dictionary to aggregate variations. Please refer to https://docs.constructor.io/rest_api/variations_mapping for details
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

        request_url = _create_autocomplete_url(query, parameters, user_parameters, self.__options)
        requests = self.__options.get('requests') or r

        response = requests.get(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options, user_parameters)
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

        raise ConstructorException('get_autocomplete_results response data is malformed')
