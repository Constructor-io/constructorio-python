'''Browse Module'''

from time import time
from urllib.parse import quote, urlencode

import requests as r

from constructorio_python.helpers.utils import (
    clean_params, create_auth_header, create_request_headers,
    create_shared_query_params, throw_http_exception_from_response)


def complete_browse_url(prefix, parameters, user_parameters, options, omit_timestamp = False):
    # pylint: disable=too-many-branches
    '''Create URL from supplied filter name, filter value, and parameters'''

    query_params = create_shared_query_params(options, user_parameters)

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

    if not omit_timestamp:
        query_params['_dt'] = int(time()*1000.0)

    query_params = clean_params(query_params)
    query_string = urlencode(query_params, doseq=True)

    return f'{options.get("service_url")}/{prefix}?{query_string}' # pylint: disable=line-too-long
    # return f'{options.get("service_url")}/browse/{quote(filter_name)}/{quote(filter_value)}?{query_string}' # pylint: disable=line-too-long

class Browse:
    '''Browse Class'''

    def __init__(self, options):
        self.__options = options or {}

    def get_browse_results(self, filter_name, filter_value, parameters=None, user_parameters=None):
        '''
        Retrieve browse results from API

        :param str filter_name: Filter name to display results from
        :param str filter_value: Filter value to display results from
        :param dict parameters: Additional parameters to refine result set
        :param int parameters.page: The page number of the results
        :param int parameters.results_per_page: The number of results per page to return
        :param dict parameters.filters: Filters used to refine results
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

        if not filter_name or not isinstance(filter_name, str):
            raise Exception('filter_name is a required parameter of type string')

        if not filter_value or not isinstance(filter_value, str):
            raise Exception('filter_value is a required parameter of type string')

        if not parameters:
            parameters = {}
        if not user_parameters:
            user_parameters = {}

        urlPrefix = f'browse/{quote(filter_name)}/{quote(filter_value)}'
        request_url = complete_browse_url(
            urlPrefix,
            parameters,
            user_parameters,
            self.__options)
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

        raise Exception('get_browse_results response data is malformed')


    def get_browse_groups(self, parameters=None, user_parameters=None):
        '''
        Retrieve groups from API

        :param dict parameters: Additional parameters to refine result set
        :param dict parameters.filters: Filters used to refine results
        :param dict parameters.fmt_options: The format options used to refine result groups
        :param int parameters.fmt_options.groups_max_depth: The maximum depth of the hierarchy group structure
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

        urlPrefix = f'browse/groups'
        request_url = complete_browse_url(
            urlPrefix,
            parameters,
            user_parameters,
            self.__options,
            True)
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
            if json_response.get('groups') or json_response.get('groups') == []:

                return json

        raise Exception('get_browse_groups response data is malformed')
