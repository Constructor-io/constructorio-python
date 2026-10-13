'''Recommendations Module'''

import json as json_lib
from time import time
from urllib.parse import quote, urlencode

import requests as r

from constructor_io.helpers.exception import ConstructorException
from constructor_io.helpers.utils import (clean_params, create_auth_header,
                                          create_request_headers,
                                          create_shared_query_params,
                                          throw_http_exception_from_response)


def _create_recommendations_url(pod_id, parameters, user_parameters, options):
    '''Create URL from supplied parameters'''

    query_params = create_shared_query_params(options, parameters, user_parameters)

    if not pod_id or not isinstance(pod_id, str):
        raise ConstructorException('pod_id is a required parameter of type string')

    if parameters:
        if parameters.get('num_results'):
            query_params['num_results'] = parameters.get('num_results')

        if parameters.get('item_ids'):
            query_params['item_id'] = parameters.get('item_ids')

        if parameters.get('term'):
            query_params['term'] = parameters.get('term')

    query_params['_dt'] = int(time()*1000.0)
    query_params = clean_params(query_params)
    query_string = urlencode(query_params, doseq=True)

    return f'{options.get("service_url")}/recommendations/v1/pods/{quote(pod_id)}?{query_string}'


PAGE_OVERRIDABLE_PARAMETERS = (
    'num_results',
    'filters',
    'filter_match_types',
    'pre_filter_expression',
    'fmt_options',
    'hidden_fields',
    'variations_map',
)


def _bracket_name(prefix, name):
    '''Nest a query parameter name under a bracket prefix'''

    return f'{prefix}[{name}]' if prefix else name


def _create_page_overridable_params(parameters, prefix=''):
    # pylint: disable=too-many-branches
    '''Create the parameters that can be set per pod, in the same wire format as the pod endpoint'''

    params = {}

    if parameters.get('num_results') is not None:
        params[_bracket_name(prefix, 'num_results')] = parameters.get('num_results')

    if parameters.get('filters'):
        filters = parameters.get('filters')
        if not isinstance(filters, dict):
            raise ConstructorException('filters must be a dictionary')
        for key, value in filters.items():
            params[f'{_bracket_name(prefix, "filters")}[{key}]'] = value

    if parameters.get('filter_match_types'):
        filter_match_types = parameters.get('filter_match_types')
        if not isinstance(filter_match_types, dict):
            raise ConstructorException('filter_match_types must be a dictionary')
        for key, value in filter_match_types.items():
            params[f'{_bracket_name(prefix, "filter_match_types")}[{key}]'] = value

    if parameters.get('hidden_fields'):
        params[f'{_bracket_name(prefix, "fmt_options")}[hidden_fields]'] = parameters.get('hidden_fields')

    if parameters.get('fmt_options'):
        fmt_options = parameters.get('fmt_options')
        if not isinstance(fmt_options, dict):
            raise ConstructorException('fmt_options must be a dictionary')
        for key, value in fmt_options.items():
            params[f'{_bracket_name(prefix, "fmt_options")}[{key}]'] = value

    if parameters.get('variations_map'):
        params[_bracket_name(prefix, 'variations_map')] = json_lib.dumps(parameters.get('variations_map'))

    if parameters.get('pre_filter_expression'):
        pre_filter_expression = parameters.get('pre_filter_expression')
        if not isinstance(pre_filter_expression, str):
            pre_filter_expression = json_lib.dumps(pre_filter_expression)
        params[_bracket_name(prefix, 'pre_filter_expression')] = pre_filter_expression

    return params


def _create_recommendation_page_url(page_id, parameters, user_parameters, options):
    '''Create page URL from supplied parameters'''

    if not page_id or not isinstance(page_id, str):
        raise ConstructorException('page_id is a required parameter of type string')

    query_params = create_shared_query_params(options, {}, user_parameters)

    if parameters.get('section'):
        query_params['section'] = parameters.get('section')

    if parameters.get('item_ids'):
        query_params['item_id'] = parameters.get('item_ids')

    if parameters.get('variation_id'):
        if not parameters.get('item_ids'):
            raise ConstructorException('item_ids is a required parameter for variation_id')
        query_params['variation_id'] = parameters.get('variation_id')

    if parameters.get('term'):
        query_params['term'] = parameters.get('term')

    query_params.update(_create_page_overridable_params(parameters))

    pod_overrides = parameters.get('pod_overrides')
    if pod_overrides:
        if not isinstance(pod_overrides, dict):
            raise ConstructorException('pod_overrides must be a dictionary keyed by pod id')
        for override_pod_id, override in pod_overrides.items():
            override = override or {}
            if not isinstance(override, dict):
                raise ConstructorException(f'pod_overrides.{override_pod_id} must be a dictionary')
            unsupported = [name for name in override if name not in PAGE_OVERRIDABLE_PARAMETERS]
            if unsupported:
                raise ConstructorException(
                    f'pod_overrides.{override_pod_id} contains parameters that cannot be overridden per pod: '
                    f'{", ".join(unsupported)}. Supported: {", ".join(PAGE_OVERRIDABLE_PARAMETERS)}'
                )
            query_params.update(
                _create_page_overridable_params(override, f'pod_overrides[{override_pod_id}]')
            )

    query_params['_dt'] = int(time()*1000.0)
    query_params = clean_params(query_params)
    query_string = urlencode(query_params, doseq=True)

    return f'{options.get("service_url")}/recommendations/v1/pages/{quote(page_id)}?{query_string}'



class Recommendations:
    '''Recommendations Class'''

    def __init__(self, options):
        self.__options = options or {}

    def get_recommendation_results(self, pod_id, parameters=None, user_parameters=None):
        '''
        Retrieve recommendation results from API

        :param str pod_id: Recommendation pod identifier
        :param dict parameters: Additional parameters to refine result set
        :param int parameters.num_results: The total number of results to return
        :param str|list parameters.item_ids: Item ID(s) to retrieve recommendations for (strategy specific)
        :param str parameters.term: The term to use to refine results (strategy specific)
        :param dict parameters.filters: Key / value mapping of filters used to refine results
        :param str parameters.section: The section to return results from
        :param dict parameters.variations_map: The variations map dictionary to aggregate variations. Please refer to https://docs.constructor.com/reference/shared-variations-mapping for details
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

        request_url = _create_recommendations_url(pod_id, parameters, user_parameters, self.__options)
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

        raise ConstructorException('get_recommendation_results response data is malformed')

    def get_recommendation_page_results(self, page_id, parameters=None, user_parameters=None):
        '''
        Retrieve recommendation results for every pod on a page from API

        Beta: available to a small group of users and may change. Contact your Customer Success
        Manager to request access.

        Each pod's own ``result_id`` is added to that pod's results. The top-level ``result_id``
        identifies the page request and is not a tracking id: send ``response.pods[].result_id``
        with each pod's recommendation view and click events.

        :param str page_id: Recommendation page identifier
        :param dict parameters: Additional parameters to refine result set, applied to every pod
        :param int parameters.num_results: The number of results to return per pod
        :param str|list parameters.item_ids: Item ID(s) to retrieve recommendations for (strategy specific)
        :param str parameters.variation_id: Variation ID to retrieve recommendations for (strategy specific)
        :param str parameters.term: The term to use to refine results (strategy specific)
        :param dict parameters.filters: Key / value mapping of filters used to refine results
        :param dict parameters.filter_match_types: Whether results must match 'all', 'any' or 'none' of each filter's values
        :param dict|str parameters.pre_filter_expression: Faceting expression to scope results
        :param dict parameters.fmt_options: Options to format the response
        :param list parameters.hidden_fields: Hidden metadata fields to return
        :param str parameters.section: The section to return results from
        :param dict parameters.variations_map: The variations map dictionary to aggregate variations. Please refer to https://docs.constructor.com/reference/shared-variations-mapping for details
        :param dict parameters.pod_overrides: Per-pod values keyed by pod id. Each may contain num_results, filters, filter_match_types, pre_filter_expression, fmt_options, hidden_fields and variations_map, and replaces (does not merge with) the page-wide value for that pod. hidden_fields is sent inside fmt_options, so either one replaces the page-wide fmt_options and hidden_fields together
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

        request_url = _create_recommendation_page_url(page_id, parameters, user_parameters, self.__options)
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

        if json_response and isinstance(json_response.get('pods'), list):
            for pod in json_response.get('pods'):
                pod_result_id = pod.get('result_id')
                pod_results = (pod.get('response') or {}).get('results')

                # Use the pod's own result_id, never the page's
                if pod_result_id and isinstance(pod_results, list):
                    for result in pod_results:
                        result['result_id'] = pod_result_id

            return json

        raise ConstructorException('get_recommendation_page_results response data is malformed')
