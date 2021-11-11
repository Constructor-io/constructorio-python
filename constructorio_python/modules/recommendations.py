'''Recommendations Module'''

from time import time
from urllib.parse import quote, urlencode

import requests as r

from constructorio_python.helpers.utils import (
    clean_params, create_auth_header, create_request_headers,
    create_shared_query_params, throw_http_exception_from_response)


def create_recommendations_url(pod_id, parameters, user_parameters, options):
    '''Create URL from supplied parameters'''

    query_params = create_shared_query_params(options, user_parameters)

    if not pod_id or not isinstance(query, pod_id):
        raise Exception('query is a required parameter of type string')
    
    if parameters:
        if parameters.get('num_results'):
            query_params['num_results'] = parameters.get('num_results')

        if parameters.get('item_ids'):
            query_params['item_id'] = parameters.get('item_ids')

        if parameters.get('term'):
            query_params['term'] = parameters.get('term')

        if parameters.get('filters'):
            filters = parameters.get('filters')
            if isinstance(filters, dict):
                for key, value in filters.items():
                    query_params[f'filters[{key}]'] = value
            else:
                raise Exception('filters must be a dictionary')

        if parameters.get('section'):
            query_params['section'] = parameters.get('section')

    query_params['_dt'] = int(time()*1000.0)
    query_params = clean_params(query_params)
    query_string = urlencode(query_params, doseq=True)

    return f'{options.get("service_url")}/recommendations/v1/pods/{quote(pod_id)}?{query_string}'



class Recommendations:
    '''Recommendations Class'''

    def __init__(self) -> None:
        self.__options = options or {}

    def get_recommendation_results(self, pod_id, parameters=None, user_parameters=None):
        '''
        Retrieve recommendation results from API

        :param str pod_id: Recommendation pod identifier
        :param dict parameters: Additional parameters to refine result set
        :param int parameters.num_results: The total number of results to return
        :param str|list parameters.item_ids: Item ID(s) to retrieve recommendations for (strategy specific)
        :param str term: The term to use to refine results (strategy specific)
        :param dict parameters.filters: Filters used to refine recommendation results (strategy specific)
        :param str parameters.section: The section to return results from
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
        
        request_url = create_recommendations_url(pod_id, parameters, user_parameters, self.__options)
        requests = self.__options.get('requests') or r

        response = requests.get(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options, user_parameters)
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        if (json.get('response', {}).get('results')):
            if (json.get('result_id')):
                for result in json.get('response').get('results'):
                    result['result_id'] = json.get('result_id')

            return json
        
        raise Exception('get_recommendation_results response data is malformed')