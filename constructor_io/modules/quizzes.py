'''Quizzes Module'''

from time import time
from urllib.parse import quote, urlencode
from urllib.request import Request

import requests as r

from constructor_io.helpers.exception import ConstructorException
from constructor_io.helpers.utils import (clean_params, create_auth_header,
                                          create_request_headers,
                                          create_shared_query_params,
                                          throw_http_exception_from_response)


def _create_quizzes_url(quizId, parameters, user_parameters, options, path):
    # pylint: disable=too-many-branches
    '''Create URL from supplied quizId and parameters'''

    query_params = {}
    ans_query_string = ''

    if not quizId or not isinstance(quizId, str):
        raise ConstructorException('quizId is a required parameter of type str')

    if path == 'finalize' and (type(parameters.get('a')) is not list or len(parameters.get('a')) == 0):
        raise ConstructorException('a is a required parameter of type list')

    if options:
        if options.get('api_key'):
            query_params['index_key'] = options.get('api_key')

    if parameters:
        if parameters.get('section'):
            query_params['section'] = parameters.get('section')
        if parameters.get('a'):
            answersParam = []
            answers = parameters.get('a')
            for questionAnswer in answers:
                answersParam.append(','.join(map(str, questionAnswer)))
            ans_query_string = urlencode({'a': answersParam}, doseq=True)

    query_params['_dt'] = int(time()*1000.0)
    query_params = clean_params(query_params)
    query_string = urlencode(query_params, doseq=True)

    return f'https://quizzes.cnstrc.com/v1/quizzes/{quote(quizId)}/{quote(path)}?{query_string}&{ans_query_string}'

class Quizzes:
    # pylint: disable=too-few-public-methods
    '''Quizzes Class'''

    def __init__(self, options):
        self.__options = options or {}

    def get_next_quiz(self, quizId, parameters=None, user_parameters=None):
        '''
        Retrieve next quiz from API

        :param str id: Quiz Id
        :param dict parameters: Additional parameters to determine next quiz
        :param list parameters.a: 2d Array of quiz answers in the format [[1],[1,2]]
        :param int parameters.section: Section for customer's product catalog
        :param dict user_parameters: Parameters relevant to the user request
        :param str user_parameters.user_ip: Origin user IP, from client
        :param str user_parameters.user_agent: Origin user agent, from client
        :return: dict
        '''

        if not parameters:
            parameters = {}
        if not user_parameters:
            user_parameters = {}

        request_url = _create_quizzes_url(quizId, parameters, user_parameters, self.__options, 'next')
        requests = self.__options.get('requests') or r

        response = requests.get(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options, user_parameters)
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        if json:
            if json.get('version_id'):
                return json

        raise ConstructorException('get_next_quiz response data is malformed')

    def get_finalize_quiz(self, quizId, parameters=None, user_parameters=None):
        '''
        Retrieve quiz results from API

        :param str id: Quiz Id
        :param dict parameters: Additional parameters to determine next quiz
        :param list parameters.a: 2d Array of quiz answers in the format [[1],[1,2]]
        :param int parameters.section: Section for customer's product catalog
        :param dict user_parameters: Parameters relevant to the user request
        :param str user_parameters.user_ip: Origin user IP, from client
        :param str user_parameters.user_agent: Origin user agent, from client
        :return: dict
        '''

        if not parameters:
            parameters = {}
        if not user_parameters:
            user_parameters = {}

        request_url = _create_quizzes_url(quizId, parameters, user_parameters, self.__options, 'finalize')
        requests = self.__options.get('requests') or r

        response = requests.get(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options, user_parameters)
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        if json:
            if json.get('version_id'):
                return json

        raise ConstructorException('get_finalize_quiz response data is malformed')

