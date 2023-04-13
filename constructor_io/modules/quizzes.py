'''Quizzes Module'''

from time import time
from urllib.parse import quote, urlencode

import requests as r

from constructor_io.helpers.exception import ConstructorException
from constructor_io.helpers.utils import (clean_params, create_auth_header,
                                          create_request_headers,
                                          create_shared_query_params,
                                          throw_http_exception_from_response)


def _create_quizzes_url(quiz_id, parameters, user_parameters, options, path):
    # pylint: disable=too-many-branches
    '''Create URL from supplied quiz_id and parameters'''
    quiz_service_url = 'https://quizzes.cnstrc.com'
    query_params = create_shared_query_params(options, {}, user_parameters)
    ans_query_string = ''

    if not quiz_id or not isinstance(quiz_id, str):
        raise ConstructorException('quiz_id is a required parameter of type str')

    if path == 'results' and (not isinstance(parameters.get('answers'), list) or len(parameters.get('answers')) == 0): # pylint: disable=line-too-long
        raise ConstructorException('answers is a required parameter of type list')

    if parameters:
        if parameters.get('section'):
            query_params['section'] = parameters.get('section')

        if parameters.get('quiz_version_id'):
            query_params['quiz_version_id'] = parameters.get('quiz_version_id')

        if parameters.get('quiz_session_id'):
            query_params['quiz_session_id'] = parameters.get('quiz_session_id')

        if parameters.get('answers'):
            answers_param = []
            answers = parameters.get('answers')

            for question_answer in answers:
                answers_param.append(','.join(map(str, question_answer)))

            ans_query_string = urlencode({'a': answers_param}, doseq=True)

    query_params['_dt'] = int(time()*1000.0)
    query_params = clean_params(query_params)
    query_string = urlencode(query_params, doseq=True)

    return f'{quiz_service_url}/v1/quizzes/{quote(quiz_id)}/{quote(path)}?{query_string}&{ans_query_string}'

class Quizzes:
    # pylint: disable=too-few-public-methods
    '''Quizzes Class'''

    def __init__(self, options):
        self.__options = options or {}

    def get_quiz_next_question(self, quiz_id, parameters=None, user_parameters=None):
        '''
        Retrieve next question from API

        :param str quiz_id: Quiz Id
        :param dict parameters: Additional parameters to determine next quiz
        :param list parameters.answers: 2d Array of quiz answers in the format [[1],[1,2]]
        :param str parameters.section: Section for customer's product catalog
        :param str parameters.quiz_version_id: Specific quiz_version_id for the quiz. Version ID will be returned with the first request and it should be passed with subsequent requests. More information can be found: https://docs.constructor.io/rest_api/quiz/using_quizzes/#quiz-versioning
        :param str parameters.quiz_session_id: Specific quiz_session_id for the quiz. Session ID will be returned with the first request and it should be passed with subsequent requests. More information can be found: https://docs.constructor.io/rest_api/quiz/using_quizzes/#quiz-sessions
        :param dict user_parameters: Parameters relevant to the user request
        :param int user_parameters.session_id: Session ID, utilized to personalize results
        :param str user_parameters.client_id: Client ID, utilized to personalize results
        :param str user_parameters.user_ip: Origin user IP, from client
        :param str user_parameters.user_agent: Origin user agent, from client
        :return: dict
        '''

        if not parameters:
            parameters = {}
        if not user_parameters:
            user_parameters = {}

        request_url = _create_quizzes_url(quiz_id, parameters, user_parameters, self.__options, 'next') # pylint: disable=line-too-long
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
            if json.get('quiz_version_id'):
                return json

        raise ConstructorException('get_quiz_next_question response data is malformed')

    def get_quiz_results(self, quiz_id, parameters=None, user_parameters=None):
        '''
        Retrieve quiz results from API

        :param str quiz_id: Quiz Id
        :param dict parameters: Additional parameters to determine next quiz
        :param list parameters.answers: 2d Array of quiz answers in the format [[1],[1,2]]
        :param str parameters.section: Section for customer's product catalog
        :param str parameters.quiz_version_id: Specific quiz_version_id for the quiz. Version ID will be returned with the first request and it should be passed with subsequent requests. More information can be found: https://docs.constructor.io/rest_api/quiz/using_quizzes/#quiz-versioning
        :param str parameters.quiz_session_id: Specific quiz_session_id for the quiz. Session ID will be returned with the first request and it should be passed with subsequent requests. More information can be found: https://docs.constructor.io/rest_api/quiz/using_quizzes/#quiz-sessions
        :param dict user_parameters: Parameters relevant to the user request
        :param int user_parameters.session_id: Session ID, utilized to personalize results
        :param str user_parameters.client_id: Client ID, utilized to personalize results
        :param str user_parameters.user_ip: Origin user IP, from client
        :param str user_parameters.user_agent: Origin user agent, from client
        :return: dict
        '''

        if not parameters:
            parameters = {}
        if not user_parameters:
            user_parameters = {}

        request_url = _create_quizzes_url(quiz_id, parameters, user_parameters, self.__options, 'results') #pylint: disable=line-too-long
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
            if json.get('quiz_version_id'):
                return json

        raise ConstructorException('get_quiz_results response data is malformed')
