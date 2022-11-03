'''ConstructorIO Python Client - Tasks Tests'''

from datetime import date, timedelta
from os import environ

import requests
from pytest import raises

from constructor_io.constructor_io import ConstructorIO
from constructor_io.helpers.exception import (ConstructorException,
                                              HttpException)

TEST_API_KEY = environ['TEST_API_KEY']
TEST_API_TOKEN = environ['TEST_API_TOKEN']
VALID_OPTIONS = { 'api_key': TEST_API_KEY, 'api_token': TEST_API_TOKEN}
CATALOG_EXAMPLES_BASE_URL = 'https://raw.githubusercontent.com/Constructor-io/integration-examples/main/catalog/' #pylint: disable=line-too-long
ITEMS = requests.get(f'{CATALOG_EXAMPLES_BASE_URL}items.csv').content

#make a replace catalog request and get task_id to use in tests
catalog = ConstructorIO(VALID_OPTIONS).catalog
catalog_response = catalog.replace_catalog({
    'items': ITEMS,
    'section': 'Products'
})
task_id = catalog_response.get('task_id')

def test_get_all_tasks_with_no_params():
    '''Should return a response with a valid total_count, tasks, status_counts'''

    catalog_response_no_params_test = catalog.replace_catalog({
        'items': ITEMS,
        'section': 'Products'
    })
    task_id_no_params_test = catalog_response_no_params_test.get('task_id')
    tasks = ConstructorIO(VALID_OPTIONS).tasks
    response = tasks.get_all_tasks()

    assert isinstance(response.get('status_counts'), dict)
    assert isinstance(response.get('tasks'), list)
    assert isinstance(response.get('total_count'), int)
    assert len(response.get('tasks')) <= 20 and len(response.get('tasks')) >= 1

    task = next(filter(lambda task: task.get('id') == task_id_no_params_test, response.get('tasks')), None)
    assert isinstance(task, dict)
    assert task.get('id') == task_id_no_params_test

def test_get_all_tasks_with_params():
    '''Should return a response with a valid total_count, tasks, status_counts'''

    tasks = ConstructorIO(VALID_OPTIONS).tasks
    response = tasks.get_all_tasks({ 'page': 2, 'results_per_page': 50 })

    assert isinstance(response.get('status_counts'), dict)
    assert isinstance(response.get('tasks'), list)
    assert isinstance(response.get('total_count'), int)
    assert len(response.get('tasks')) <= 50 and len(response.get('tasks')) >= 1

def test_get_all_tasks_with_start_date_and_end_date():
    '''Should return a response when start_date and end_date are passed'''

    curDate = date.today();
    endDate = curDate.strftime('%Y-%m-%d')
    startDate = (curDate - timedelta(days=30)).strftime('%Y-%m-%d')

    tasks = ConstructorIO(VALID_OPTIONS).tasks
    response = tasks.get_all_tasks({ 'start_date': startDate, 'end_date': endDate })

    assert isinstance(response.get('status_counts'), dict)
    assert isinstance(response.get('tasks'), list)
    assert isinstance(response.get('total_count'), int)
    assert len(response.get('tasks')) <= 50 and len(response.get('tasks')) >= 1

def test_get_all_tasks_with_status():
    '''Should return a response when status is passed'''

    tasks = ConstructorIO(VALID_OPTIONS).tasks
    response = tasks.get_all_tasks({ 'status': 'DONE' })

    assert isinstance(response.get('status_counts'), dict)
    assert isinstance(response.get('tasks'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('tasks')[0].get('status') == 'DONE'
    assert len(response.get('tasks')) <= 50 and len(response.get('tasks')) >= 1

def test_get_all_tasks_with_type():
    '''Should return a response when status is passed'''

    tasks = ConstructorIO(VALID_OPTIONS).tasks
    response = tasks.get_all_tasks({ 'type': 'ingestion' })

    assert isinstance(response.get('status_counts'), dict)
    assert isinstance(response.get('tasks'), list)
    assert isinstance(response.get('total_count'), int)
    assert len(response.get('tasks')) <= 50 and len(response.get('tasks')) >= 1

def test_get_all_tasks_with_invalid_api_key():
    '''Should raise exception when invalid api_key is provided'''

    with raises(
        HttpException,
        match=r'You have supplied an invalid `key` or `autocomplete_key`. You can find your key at app.constructor.io/dashboard/accounts/api_integration.' # pylint: disable=line-too-long
    ):
        tasks = ConstructorIO({ 'api_key': 'invalidkey', 'api_token': TEST_API_TOKEN}).tasks
        tasks.get_all_tasks()

def test_get_all_tasks_with_invalid_api_token():
    '''Should raise exception when invalid api_token is provided'''

    with raises(
        HttpException,
        match=r'Invalid auth_token. If you\'ve forgotten your token, you can generate a new one at app.constructor.io/dashboard' # pylint: disable=line-too-long
    ):
        tasks = ConstructorIO({ 'api_key': TEST_API_KEY, 'api_token': 'invalidapitoken'}).tasks
        tasks.get_all_tasks()

def test_get_task_with_task_id():
    '''Should return result when valid task_id is provided'''

    tasks = ConstructorIO(VALID_OPTIONS).tasks
    response = tasks.get_task(task_id)

    assert isinstance(response.get('id'), int)
    assert response.get('id') == task_id
    assert isinstance(response.get('status'), str)
    assert isinstance(response.get('submission_time'), str)

def task_get_task_without_task_id():
    '''Should raise exception when no task_id is provided'''

    with raises(
        ConstructorException,
        match=r'task_id is a required parameter of type int'
    ):
        tasks = ConstructorIO(VALID_OPTIONS).tasks
        tasks.get_task(None)

def test_get_task_with_invalid_api_key():
    '''Should raise exception when invalid api_key is provided'''

    with raises(
        HttpException,
        match=r'You have supplied an invalid `key` or `autocomplete_key`. You can find your key at app.constructor.io/dashboard/accounts/api_integration.' # pylint: disable=line-too-long
    ):
        tasks = ConstructorIO({ 'api_key': 'invalidkey', 'api_token': TEST_API_TOKEN}).tasks
        tasks.get_task(1)

def test_get_task_with_invalid_api_token():
    '''Should raise exception when invalid api_token is provided'''

    with raises(
        HttpException,
        match=r'Invalid auth_token. If you\'ve forgotten your token, you can generate a new one at app.constructor.io/dashboard' # pylint: disable=line-too-long
    ):
        tasks = ConstructorIO({ 'api_key': TEST_API_KEY, 'api_token': 'invalidapitoken'}).tasks
        tasks.get_task(1)
