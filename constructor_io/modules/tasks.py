'''Tasks Module'''

from urllib.parse import quote, urlencode

import requests as r

from constructor_io.helpers.exception import ConstructorException
from constructor_io.helpers.utils import (clean_params, create_auth_header,
                                          create_request_headers,
                                          create_shared_query_params,
                                          throw_http_exception_from_response)


def _create_tasks_url(url_prefix, parameters, options, api_version='v1'):
    '''Create URL from supplied url_prefix and parameters'''

    query_params = create_shared_query_params(options, parameters, {})
    query_params.pop('c')

    if parameters:
        if parameters.get('start_date'):
            query_params['start_date'] = parameters.get('start_date')

        if parameters.get('end_date'):
            query_params['end_date'] = parameters.get('end_date')

        if parameters.get('status'):
            query_params['status'] = parameters.get('status')

        if parameters.get('type'):
            query_params['type'] = parameters.get('type')

    query_params = clean_params(query_params)
    query_string = urlencode(query_params, doseq=True)

    return f'{options.get("service_url")}/{api_version}/{url_prefix}?{query_string}'

class Tasks:
    # pylint: disable=too-few-public-methods
    '''Tasks Class'''

    def __init__(self, options) -> None:
        self.__options = options or {}

    def get_all_tasks(self, parameters=None):
        '''
        Retrieve tasks from API

        :param dict parameters: Additional parameters for task details
        :param int parameters.page: The page number of the results
        :param string parameters.start_date: The start date of results to return - YYYY-MM-DD
        :param string parameters.end_date: The end date of results to return - YYYY-MM-DD
        :param string parameters.status: The status of tasks to return - 'QUEUED', 'IN_PROGRESS', 'DONE', 'FAILED', 'CANCELED'
        :param string parameters.type: The type of tasks to return - 'ingestion', 'user_data_request'
        :param int parameters.results_per_page: The number of results per page to return
        :return: dict
        '''

        if not parameters:
            parameters = {}

        url_prefix = 'tasks'
        request_url = _create_tasks_url(url_prefix, parameters, self.__options)
        requests = self.__options.get('requests') or r

        response = requests.get(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options)
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        if json:
            if json.get('total_count'):
                return json

        raise ConstructorException('get_all_tasks response data is malformed')

    def get_task(self, task_id):
        '''
        Retrieve specific task from API

        :param int task_id: The id of the task to retrieve
        :return: dict
        '''
        if not task_id or not isinstance(task_id, int):
            raise ConstructorException('task_id is a required parameter of type int')

        url_prefix = f'tasks/{quote(str(task_id))}'
        request_url = _create_tasks_url(url_prefix, None, self.__options)
        requests = self.__options.get('requests') or r

        response = requests.get(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options)
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        if json:
            if json.get('status'):
                return json

        raise ConstructorException('get_task response data is malformed')
