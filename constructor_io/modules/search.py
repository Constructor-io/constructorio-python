'''Search Module'''

from time import time
from urllib.parse import quote, urlencode

import requests as r

from constructor_io.helpers.exception import ConstructorException
from constructor_io.helpers.utils import (clean_params, create_auth_header,
                                          create_request_headers,
                                          create_shared_query_params,
                                          throw_http_exception_from_response)


def _create_search_url(query, parameters, user_parameters, options):
    # pylint: disable=too-many-branches
    '''Create URL from supplied query (term) and parameters'''

    query_params = create_shared_query_params(options, parameters, user_parameters)

    if not query or not isinstance(query, str):
        raise ConstructorException('query is a required parameter of type string')

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
        :param list parameters.hidden_facets: Hidden facet fields to return
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

        request_url = _create_search_url(query, parameters, user_parameters, self.__options)
        requests = self.__options.get('requests') or r

        response = requests.get(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options, user_parameters)
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

        raise ConstructorException('get_search_results response data is malformed')
