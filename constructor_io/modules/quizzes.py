'''Quizzes Module'''

from time import time
from urllib.parse import quote, urlencode

import requests as r

from constructor_io.helpers.exception import ConstructorException
from constructor_io.helpers.utils import (clean_params, create_auth_header,
                                          create_request_headers,
                                          throw_http_exception_from_response)


def _create_quizzes_url(quiz_id, parameters, options, path):
    # pylint: disable=too-many-branches
    '''Create URL from supplied quiz_id and parameters'''
    quiz_service_url = 'https://quizzes.cnstrc.com/v1/quizzes'
    query_params = {}
    ans_query_string = ''

    if not quiz_id or not isinstance(quiz_id, str):
        raise ConstructorException('quiz_id is a required parameter of type str')

    if path == 'finalize' and (isinstance(parameters.get('a'), list) or len(parameters.get('a')) == 0): # pylint: disable=line-too-long
        raise ConstructorException('a is a required parameter of type list')

    if options:
        if options.get('api_key'):
            query_params['index_key'] = options.get('api_key')

    if parameters:
        if parameters.get('section'):
            query_params['section'] = parameters.get('section')
        if parameters.get('a'):
            answers_param = []
            answers = parameters.get('a')
            for question_answer in answers:
                answers_param.append(','.join(map(str, question_answer)))
            ans_query_string = urlencode({'a': answers_param}, doseq=True)

    query_params['_dt'] = int(time()*1000.0)
    query_params = clean_params(query_params)
    query_string = urlencode(query_params, doseq=True)

    return f'{quiz_service_url}/{quote(quiz_id)}/{quote(path)}?{query_string}&{ans_query_string}'

class Quizzes:
    # pylint: disable=too-few-public-methods
    '''Quizzes Class'''

    def __init__(self, options):
        self.__options = options or {}

    def get_next_quiz(self, quiz_id, parameters=None, user_parameters=None):
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

        request_url = _create_quizzes_url(quiz_id, parameters, self.__options, 'next') # pylint: disable=line-too-long
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

    def get_finalize_quiz(self, quiz_id, parameters=None, user_parameters=None):
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

        request_url = _create_quizzes_url(quiz_id, parameters, self.__options, 'finalize') #pylint: disable=line-too-long
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
