'''Browse Module'''

from time import time
from urllib.parse import quote, urlencode

import requests as r

from constructor_io.helpers.exception import ConstructorException
from constructor_io.helpers.utils import (clean_params, create_auth_header,
                                          create_request_headers,
                                          create_shared_query_params,
                                          throw_http_exception_from_response)


def _create_browse_url(prefix, parameters, user_parameters, options, omit_timestamp = False):
    # pylint: disable=too-many-branches
    '''Create URL from supplied filter name, filter value, and parameters'''

    query_params = create_shared_query_params(options, parameters, user_parameters)

    if parameters:
        if parameters.get('item_ids'):
            query_params['ids'] = parameters.get('item_ids')
        if parameters.get('facet_name'):
            query_params['facet_name'] = parameters.get('facet_name')

    if not omit_timestamp:
        query_params['_dt'] = int(time()*1000.0)

    query_params = clean_params(query_params)
    query_string = urlencode(query_params, doseq=True)

    return f'{options.get("service_url")}/{prefix}?{query_string}'

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

        if not filter_name or not isinstance(filter_name, str):
            raise ConstructorException('filter_name is a required parameter of type string')

        if not filter_value or not isinstance(filter_value, str):
            raise ConstructorException('filter_value is a required parameter of type string')

        if not parameters:
            parameters = {}
        if not user_parameters:
            user_parameters = {}

        url_prefix = f'browse/{quote(filter_name)}/{quote(filter_value)}'
        request_url = _create_browse_url(
            url_prefix,
            parameters,
            user_parameters,
            self.__options
        )

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

        raise ConstructorException('get_browse_results response data is malformed')


    def get_browse_results_for_item_ids(self, item_ids, parameters=None, user_parameters=None):
        '''
        Retrieve browse results from API using item ID's

        :param list item_ids: Item ID's of results to get results for
        :param dict parameters: Additional parameters to refine result set
        :param int parameters.page: The page number of the results
        :param int parameters.results_per_page: The number of results per page to return
        :param dict parameters.filters: Filters used to refine results
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

        if not item_ids or not isinstance(item_ids, list):
            raise ConstructorException('item_ids is a required parameter of type list')

        if not parameters:
            parameters = {}
        if not user_parameters:
            user_parameters = {}

        url_prefix = 'browse/items'
        request_url = _create_browse_url(
            url_prefix,
            { **parameters, 'item_ids': item_ids},
            user_parameters,
            self.__options
        )
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

        raise ConstructorException('get_browse_results_for_item_ids response data is malformed')


    def get_browse_groups(self, parameters=None, user_parameters=None):
        '''
        Retrieve groups from API

        :param dict parameters: Additional parameters to refine result set
        :param dict parameters.filters: Filters used to refine results
        :param str parameters.section: Section name for results
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

        url_prefix = 'browse/groups'
        request_url = _create_browse_url(
            url_prefix,
            parameters,
            user_parameters,
            self.__options,
            True
        )
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

        raise ConstructorException('get_browse_groups response data is malformed')


    def get_browse_facets(self, parameters=None, user_parameters=None):
        '''
        Retrieve facets from API

        :param dict parameters: Additional parameters to refine result set
        :param dict parameters.page: The page number of the results
        :param dict parameters.results_per_page: The number of results per page to return
        :param str parameters.section: Section name for results
        :param dict parameters.fmt_options: The format options used to refine result groups
        :param int parameters.fmt_options.show_hidden_facets: Include facets configured as hidden
        :param int parameters.fmt_options.show_protected_facets: Include facets configured as protected
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

        url_prefix = 'browse/facets'
        request_url = _create_browse_url(
            url_prefix,
            parameters,
            user_parameters,
            self.__options,
            True
        )
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
            if json_response.get('facets') or json_response.get('facets') == []:
                return json

        raise ConstructorException('get_browse_facets response data is malformed')

    def get_browse_facet_options(self, facet_name, parameters=None, user_parameters=None):
        '''
        Retrieve facet options for a given facet group from the API

        :param str facet_name: Name of the facet whose options to return
        :param dict parameters: Additional parameters to refine result set
        :param str parameters.section: Section name for results
        :param dict parameters.fmt_options: The format options used to refine result groups
        :param int parameters.fmt_options.show_hidden_facets: Include facets configured as hidden
        :param int parameters.fmt_options.show_protected_facets: Include facets configured as protected
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
        if not facet_name or not isinstance(facet_name, str):
            raise ConstructorException('facet_name is a required parameter of type string')

        if not parameters:
            parameters = {}
        if not user_parameters:
            user_parameters = {}

        url_prefix = 'browse/facet_options'
        request_url = _create_browse_url(
            url_prefix,
            { **parameters, 'facet_name': facet_name},
            user_parameters,
            self.__options,
            True
        )
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
            if json_response.get('facets') or json_response.get('facets') == []:
                return json

        raise ConstructorException('get_browse_facet_options response data is malformed')
