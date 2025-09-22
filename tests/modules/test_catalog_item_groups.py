'''ConstructorIO Python Client - Item Groups Catalog Tests'''

from os import environ
from time import sleep

import pytest
from pytest import raises

from constructor_io.constructor_io import ConstructorIO
from constructor_io.helpers.exception import HttpException
from tests.helpers.utils import create_mock_item_group

TEST_API_KEY = environ['TEST_CATALOG_API_KEY']
TEST_API_TOKEN = environ['TEST_API_TOKEN']
VALID_OPTIONS = { 'api_key': TEST_API_KEY, 'api_token': TEST_API_TOKEN }
SECTION = 'Products'

@pytest.fixture(autouse=True)
def slow_down_tests():
    '''Sleep between tests'''

    yield
    sleep(1)

def test_create_or_replace_item_groups():
    '''Should create new item groups'''

    constructorIO = ConstructorIO(VALID_OPTIONS)
    catalog = constructorIO.catalog
    tasks = constructorIO.tasks

    item_groups = [
        create_mock_item_group(),
        create_mock_item_group()
    ]
    parameters = {
        'item_groups': item_groups
    }

    response = catalog.create_or_replace_item_groups(parameters)

    assert response is not None

    task_id = response.get('task_id')
    task = tasks.get_task(task_id)

    assert task.get('status') in ['QUEUED', 'IN_PROGRESS', 'DONE']

def test_create_or_replace_item_groups_with_all_parameters():
    '''Should create new item groups with all parameters'''

    constructorIO = ConstructorIO(VALID_OPTIONS)
    catalog = constructorIO.catalog
    tasks = constructorIO.tasks

    item_groups = [
        create_mock_item_group(),
        create_mock_item_group()
    ]
    parameters = {
        'item_groups': item_groups,
        'notification_email': 'test@constructor.io',
        'force': True,
    }

    response = catalog.create_or_replace_item_groups(parameters)

    assert response is not None

    task_id = response.get('task_id')
    task = tasks.get_task(task_id)

    assert task.get('status') in ['QUEUED', 'IN_PROGRESS', 'DONE']

def test_create_or_replace_item_groups_validation():
    '''Should validate item_groups parameter requirements'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    # Test with missing item_groups parameter
    with raises(
        HttpException,
        match=r'item_groups: none is not an allowed value'
    ):
        catalog.create_or_replace_item_groups({})

    # Test with empty item_groups array
    with raises(
        HttpException,
        match=r'item_groups: ensure this value has at least 1 items'
    ):
        catalog.create_or_replace_item_groups({'item_groups': []})

    # Test with non-array item_groups
    with raises(
        HttpException,
        match=r'item_groups: value is not a valid list'
    ):
        catalog.create_or_replace_item_groups({'item_groups': 'not an array'})

def test_update_item_groups():
    '''Should update item groups'''

    constructorIO = ConstructorIO(VALID_OPTIONS)
    catalog = constructorIO.catalog
    tasks = constructorIO.tasks

    item_1 = create_mock_item_group()
    item_2 = create_mock_item_group()

    item_groups = [
        item_1,
        item_2
    ]
    create_parameters = {
        'item_groups': item_groups
    }

    create_response = catalog.create_or_replace_item_groups(create_parameters)

    sleep(2)

    assert create_response is not None

    item_1['name'] = 'Updated Item 1'
    item_2['name'] = 'Updated Item 2'

    update_parameters = {
        'item_groups': item_groups
    }

    update_response = catalog.update_item_groups(update_parameters)

    assert update_response is not None

    task_id = update_response.get('task_id')
    task = tasks.get_task(task_id)

    assert task.get('status') in ['QUEUED', 'IN_PROGRESS', 'DONE']

def test_update_item_groups_with_all_parameters():
    '''Should update item groups with all parameters'''

    constructorIO = ConstructorIO(VALID_OPTIONS)
    catalog = constructorIO.catalog
    tasks = constructorIO.tasks

    item_1 = create_mock_item_group()
    item_2 = create_mock_item_group()

    item_groups = [
        item_1,
        item_2
    ]
    create_parameters = {
        'item_groups': item_groups
    }

    create_response = catalog.create_or_replace_item_groups(create_parameters)

    sleep(2)

    assert create_response is not None

    item_1['name'] = 'Updated Item 1'
    item_2['name'] = 'Updated Item 2'

    update_parameters = {
        'item_groups': item_groups,
        'notification_email': 'test@constructor.io',
        'force': True,
    }

    update_response = catalog.update_item_groups(update_parameters)

    assert update_response is not None

    task_id = update_response.get('task_id')
    task = tasks.get_task(task_id)

    assert task.get('status') in ['QUEUED', 'IN_PROGRESS', 'DONE']

def test_update_item_groups_validation():
    '''Should validate item_groups parameter requirements'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    # Test with missing item_groups parameter
    with raises(
        HttpException,
        match=r'item_groups: none is not an allowed value'
    ):
        catalog.update_item_groups({})

    # Test with empty item_groups array
    with raises(
        HttpException,
        match=r'item_groups: ensure this value has at least 1 items'
    ):
        catalog.update_item_groups({'item_groups': []})

    # Test with non-array item_groups
    with raises(
        HttpException,
        match=r'item_groups: value is not a valid list'
    ):
        catalog.update_item_groups({'item_groups': 'not an array'})

def test_retrieve_item_group():
    '''Should retrieve item group'''

    constructorIO = ConstructorIO(VALID_OPTIONS)
    catalog = constructorIO.catalog

    item_group = create_mock_item_group()

    item_groups = [item_group]
    parameters = {
        'item_groups': item_groups
    }

    response = catalog.create_or_replace_item_groups(parameters)

    assert response is not None

    sleep(2)

    retrieve_response = catalog.retrieve_item_group({
        'item_group_id': item_group['id']
    })

    assert retrieve_response is not None
    assert retrieve_response['id'] == item_group['id']

def test_retrieve_item_groups():
    '''Should retrieve all item groups'''

    constructorIO = ConstructorIO(VALID_OPTIONS)
    catalog = constructorIO.catalog

    item_groups = [
        create_mock_item_group(),
        create_mock_item_group()
    ]
    parameters = {
        'item_groups': item_groups
    }

    response = catalog.create_or_replace_item_groups(parameters)

    assert response is not None

    sleep(2)

    retrieve_response = catalog.retrieve_item_groups()

    assert retrieve_response is not None
    assert 'item_groups' in retrieve_response
    assert len(retrieve_response['item_groups']) > 0

