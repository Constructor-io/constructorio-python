'''ConstructorIO Python Client - Quizzes Tests'''

from os import environ

from pytest import raises

from constructor_io.constructor_io import ConstructorIO
from constructor_io.helpers.exception import (ConstructorException,
                                              HttpException)

TEST_API_KEY = environ['TEST_API_KEY']
TEST_API_TOKEN = environ['TEST_API_TOKEN']
QUIZ_ID = 'test-quiz'
VALID_QUIZ_ANS = [[1], [1, 2], ['seen']]
VALID_OPTIONS = { 'api_key': TEST_API_KEY, 'api_token': TEST_API_TOKEN}

def test_get_next_quiz_with_valid_parameters():
    '''Should return a response with a valid quiz_id'''

    quizzes = ConstructorIO(VALID_OPTIONS).quizzes
    response = quizzes.get_next_question('test-quiz')

    assert isinstance(response.get('version_id'), str)
    assert isinstance(response.get('next_question'), dict)

def test_get_quiz_results_with_valid_parameters():
    '''Should return a response with a valid quiz_id, a(answers)'''

    quizzes = ConstructorIO(VALID_OPTIONS).quizzes
    response = quizzes.get_quiz_results(QUIZ_ID, {'a': VALID_QUIZ_ANS})

    assert isinstance(response.get('version_id'), str)
    assert isinstance(response.get('result'), dict)
    assert isinstance(response.get('result').get('results_url'), str)

def test_get_next_quiz_with_no_quiz_id():
    '''Should raise an exception with no quiz_id'''

    with raises(
        ConstructorException,
        match=r'quiz_id is a required parameter of type str'
    ):
        quizzes = ConstructorIO(VALID_OPTIONS).quizzes
        quizzes.get_next_question(None)

def test_get_quiz_results_with_no_quiz_id():
    '''Should raise an exception with no quiz_id'''

    with raises(
        ConstructorException,
        match=r'quiz_id is a required parameter of type str'
    ):
        quizzes = ConstructorIO(VALID_OPTIONS).quizzes
        quizzes.get_quiz_results(None)

def test_get_quiz_results_with_invalid_key():
    '''Should raise an exception given invalid index_key/api_key'''

    with raises(
        HttpException,
        match=r'The quiz you requested, "test-quiz" was not found, please specify a valid quiz id before trying again.' # pylint: disable=line-too-long
    ):
        quizzes = ConstructorIO({'api_key': 'notavalidkey', 'api_token': TEST_API_TOKEN}).quizzes
        quizzes.get_quiz_results(QUIZ_ID, {'a': VALID_QUIZ_ANS})

def test_get_next_quiz_with_invalid_key():
    '''Should raise an exception given invalid index_key/api_key'''

    with raises(
        HttpException,
        match=r'The quiz you requested, "test-quiz" was not found, please specify a valid quiz id before trying again.' # pylint: disable=line-too-long
    ):
        quizzes = ConstructorIO({'api_key': 'notavalidkey', 'api_token': TEST_API_TOKEN}).quizzes
        quizzes.get_next_question(QUIZ_ID, {'a': VALID_QUIZ_ANS})

def test_get_quiz_results_with_no_answers():
    '''Should raise an exception given an empty/nonexistent answers parameter'''

    with raises(
        ConstructorException,
        match=r'a is a required parameter of type list'
    ):
        quizzes = ConstructorIO(VALID_OPTIONS).quizzes
        quizzes.get_quiz_results(QUIZ_ID, {'a': []})
