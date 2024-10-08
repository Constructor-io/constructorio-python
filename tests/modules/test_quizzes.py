'''ConstructorIO Python Client - Quizzes Tests'''

from os import environ

from pytest import raises

from constructor_io.constructor_io import ConstructorIO
from constructor_io.helpers.exception import (ConstructorException,
                                              HttpException)

TEST_API_KEY = environ['TEST_REQUEST_API_KEY']
TEST_API_TOKEN = environ['TEST_API_TOKEN']
QUIZ_ID = 'test-quiz'
QUIZ_SESSION_ID = 'ca380401-3805-4ded-8f28-638e5a4baa92'
VALID_QUIZ_ANS = [[1], [1, 2], ['seen']]
VALID_OPTIONS = { 'api_key': TEST_API_KEY, 'api_token': TEST_API_TOKEN}

def test_get_quiz_next_question_with_valid_parameters():
    '''Should return a response with a valid quiz_id'''

    quizzes = ConstructorIO(VALID_OPTIONS).quizzes
    response = quizzes.get_quiz_next_question('test-quiz')

    assert isinstance(response.get('quiz_id'), str)
    assert isinstance(response.get('quiz_version_id'), str)
    assert isinstance(response.get('quiz_session_id'), str)
    assert isinstance(response.get('next_question'), dict)

def test_get_quiz_next_question_should_respond_with_matching_parameters():
    '''Should return a response with a matching quiz_id, quiz_version_id, quiz_session_id'''

    quizzes = ConstructorIO(VALID_OPTIONS).quizzes
    initial_response = quizzes.get_quiz_next_question(QUIZ_ID, {
        'quiz_session_id': QUIZ_SESSION_ID
        })
    quiz_version_id = initial_response.get('quiz_version_id')

    response = quizzes.get_quiz_next_question(QUIZ_ID, {
        'quiz_version_id': quiz_version_id,
        'quiz_session_id': QUIZ_SESSION_ID
        })

    assert response.get('quiz_id') == QUIZ_ID
    assert response.get('quiz_version_id') == quiz_version_id
    assert response.get('quiz_session_id') == QUIZ_SESSION_ID

def test_get_quiz_next_question_with_answer_parameter():
    '''Should return a response with a valid quiz_id and answer parameter'''

    quizzes = ConstructorIO(VALID_OPTIONS).quizzes
    response = quizzes.get_quiz_next_question('test-quiz', { 'answers': VALID_QUIZ_ANS })

    assert isinstance(response.get('quiz_id'), str)
    assert isinstance(response.get('quiz_version_id'), str)
    assert isinstance(response.get('quiz_session_id'), str)
    assert isinstance(response.get('next_question'), dict)
    assert response.get('next_question').get('id') == 4

def test_get_quiz_next_question_with_no_quiz_id():
    '''Should raise an exception with no quiz_id'''

    with raises(
        ConstructorException,
        match=r'quiz_id is a required parameter of type str'
    ):
        quizzes = ConstructorIO(VALID_OPTIONS).quizzes
        quizzes.get_quiz_next_question(None)

def test_get_quiz_next_question_with_invalid_quiz_id():
    '''Should raise an exception with invalid quiz_id'''

    with raises(
        ConstructorException,
        match=r'The quiz you requested, "abcd" was not found, please specify a valid quiz id before trying again.' # pylint: disable=line-too-long
    ):
        quizzes = ConstructorIO(VALID_OPTIONS).quizzes
        quizzes.get_quiz_next_question('abcd')

def test_get_quiz_next_question_with_invalid_key():
    '''Should raise an exception given invalid index_key/api_key'''

    with raises(
        ConstructorException,
        match=r'The quiz you requested, "test-quiz" was not found, please specify a valid quiz id before trying again.' # pylint: disable=line-too-long
    ):
        quizzes = ConstructorIO({'api_key': 'notavalidkey', 'api_token': TEST_API_TOKEN}).quizzes
        quizzes.get_quiz_next_question(QUIZ_ID, {'answers': VALID_QUIZ_ANS})

def test_get_quiz_results_with_valid_parameters():
    '''Should return a response with a valid quiz_id, a(answers)'''

    quizzes = ConstructorIO(VALID_OPTIONS).quizzes
    res = quizzes.get_quiz_results(QUIZ_ID, {'answers': VALID_QUIZ_ANS})
    request = res.get('request')
    response = res.get('response')

    assert isinstance(res.get('quiz_id'), str)
    assert isinstance(res.get('quiz_version_id'), str)
    assert isinstance(res.get('quiz_session_id'), str)
    assert isinstance(res.get('result_id'), str)
    assert isinstance(request, dict)
    assert isinstance(response, dict)
    assert isinstance(response.get('total_num_results'), int)
    assert isinstance(response.get('result_sources'), dict)
    assert isinstance(response.get('results'), list)
    assert isinstance(response.get('sort_options'), list)
    assert isinstance(response.get('facets'), list)
    assert isinstance(response.get('groups'), list)
    assert isinstance(response.get('refined_content'), list)
    assert isinstance(response.get('total_num_results'), int)

def test_get_quiz_results_should_respond_with_matching_parameters():
    '''Should return a response with a matching quiz_id, quiz_version_id, quiz_session_id'''

    quizzes = ConstructorIO(VALID_OPTIONS).quizzes
    initial_response = quizzes.get_quiz_next_question(QUIZ_ID, {
        'quiz_session_id': QUIZ_SESSION_ID
        })
    quiz_version_id = initial_response.get('quiz_version_id')

    res = quizzes.get_quiz_results(QUIZ_ID, {
        'answers': VALID_QUIZ_ANS,
        'quiz_version_id': quiz_version_id,
        'quiz_session_id': QUIZ_SESSION_ID})

    assert res.get('quiz_id') == QUIZ_ID
    assert res.get('quiz_version_id') == quiz_version_id
    assert res.get('quiz_session_id') == QUIZ_SESSION_ID

def test_get_quiz_results_with_no_quiz_id():
    '''Should raise an exception with no quiz_id'''

    with raises(
        ConstructorException,
        match=r'quiz_id is a required parameter of type str'
    ):
        quizzes = ConstructorIO(VALID_OPTIONS).quizzes
        quizzes.get_quiz_results(None)

def test_get_quiz_results_with_invalid_quiz_id():
    '''Should raise an exception given invalid quiz_id'''

    with raises(
        HttpException,
        match=r'The quiz you requested, "abcd" was not found, please specify a valid quiz id before trying again.' # pylint: disable=line-too-long
    ):
        quizzes = ConstructorIO({'api_key': 'notavalidkey', 'api_token': TEST_API_TOKEN}).quizzes
        quizzes.get_quiz_results('abcd', {'answers': VALID_QUIZ_ANS})

def test_get_quiz_results_with_invalid_key():
    '''Should raise an exception given invalid index_key/api_key'''

    with raises(
        HttpException,
        match=r'The quiz you requested, "test-quiz" was not found, please specify a valid quiz id before trying again.' # pylint: disable=line-too-long
    ):
        quizzes = ConstructorIO({'api_key': 'notavalidkey', 'api_token': TEST_API_TOKEN}).quizzes
        quizzes.get_quiz_results(QUIZ_ID, {'answers': VALID_QUIZ_ANS})

def test_get_quiz_results_with_empty_answers():
    '''Should raise an exception given an empty answers parameter'''

    with raises(
        ConstructorException,
        match=r'answers is a required parameter of type list'
    ):
        quizzes = ConstructorIO(VALID_OPTIONS).quizzes
        quizzes.get_quiz_results(QUIZ_ID, {'answers': []})

def test_get_quiz_results_with_no_answers():
    '''Should raise an exception given an nonexistent answers parameter'''

    with raises(
        ConstructorException,
        match=r'answers is a required parameter of type list'
    ):
        quizzes = ConstructorIO(VALID_OPTIONS).quizzes
        quizzes.get_quiz_results(QUIZ_ID, { })
