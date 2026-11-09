'''Tracker Module'''

from time import time
from urllib.parse import urlencode

import requests as r

from constructor_io.helpers.exception import ConstructorException
from constructor_io.helpers.utils import (clean_params, create_request_headers,
                                          create_shared_query_params,
                                          throw_http_exception_from_response)


class Tracker:
    # pylint: disable=too-few-public-methods
    '''Tracker Class'''

    def __init__(self, options) -> None:
        self.__options = options or {}

    def track_search_results_loaded(self, term, parameters=None, user_parameters=None):
        '''
        Send search results loaded event to API

        :param str term: Search query term
        :param dict parameters: Additional parameters to be sent with request
        :param int parameters.result_count: Total number of results (defaults to the number of items)
        :param str parameters.result_id: Result ID from the search response
        :param list parameters.items: Items shown, as item ids or dicts with item_id and optional variation_id (max 100)
        :param int parameters.result_page: Page number of the results
        :param str parameters.section: Section name for results
        :param str parameters.url: Current page URL
        :param dict user_parameters: Parameters relevant to the user request
        :param int user_parameters.session_id: Session ID (required)
        :param str user_parameters.client_id: Client ID (required)
        :param str user_parameters.user_id: User ID, utilized to personalize results
        :param str user_parameters.segments: User segments
        :param dict user_parameters.test_cells: User test cells
        :param str user_parameters.user_ip: Origin user IP, from client
        :param str user_parameters.user_agent: Origin user agent, from client

        :return: bool
        '''

        if not parameters:
            parameters = {}
        if not user_parameters:
            user_parameters = {}

        if not term or not isinstance(term, str):
            raise ConstructorException('term is a required parameter of type string')
        if not user_parameters.get('client_id') or not isinstance(user_parameters.get('client_id'), str):
            raise ConstructorException('client_id is a required user parameter of type string')
        if not user_parameters.get('session_id') or not isinstance(user_parameters.get('session_id'), int):
            raise ConstructorException('session_id is a required user parameter of type int')

        query_params = create_shared_query_params(self.__options, {}, user_parameters)
        query_params['_dt'] = int(time()*1000.0)
        query_params['beacon'] = 'true'
        query_params = clean_params(query_params)

        items = parameters.get('items') or []
        items = [{'item_id': str(item)} if isinstance(item, (str, int)) else item for item in items[:100]]

        body = {
            **query_params,
            'beacon': True,
            'search_term': term,
            'result_count': parameters.get('result_count', len(items)),
            'result_id': parameters.get('result_id'),
            'items': items or None,
            'result_page': parameters.get('result_page'),
            'section': parameters.get('section'),
            'url': parameters.get('url') or 'N/A',
        }
        body = {key: value for key, value in body.items() if value is not None}

        request_url = (
            f'{self.__options.get("service_url")}/v2/behavioral_action/search_result_load?'
            f'{urlencode(query_params, doseq=True)}'
        )
        requests = self.__options.get('requests') or r

        response = requests.post(
            request_url,
            json=body,
            headers=create_request_headers(self.__options, user_parameters)
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        return True
