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

def test_create_item_groups():
    '''Should create new item groups'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    item_groups = [
        create_mock_item_group(),
        create_mock_item_group()
    ]
    parameters = {
        'item_groups': item_groups
    }

    response = catalog.create_item_groups(parameters)

    assert response is not None

    stats = response['item_groups']
    expected_stats = {
        'processed': 2,
        'inserted': 2,
        'deleted': 0,
        'updated': 0
    }

    assert stats == expected_stats

    catalog.delete_item_groups()

def test_create_item_groups_validation():
    '''Should validate item_groups parameter requirements'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    # Test with missing item_groups parameter
    with raises(
        HttpException,
        match=r'item_groups: none is not an allowed value'
    ):
        catalog.create_item_groups({})

    # Test with empty item_groups array
    with raises(
        HttpException,
        match=r'item_groups: ensure this value has at least 1 items'
    ):
        catalog.create_item_groups({'item_groups': []})

    # Test with non-array item_groups
    with raises(
        HttpException,
        match=r'item_groups: value is not a valid list'
    ):
        catalog.create_item_groups({'item_groups': 'not an array'})

def test_create_or_replace_item_groups():
    '''Should create or replace item groups'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    initial_item_groups = [
        create_mock_item_group(),
        create_mock_item_group(),
    ]
    parameters = {
        'item_groups': initial_item_groups
    }

    response = catalog.create_item_groups(parameters)

    updated_item_groups = [
        # Keep one existing item group but modify it
        {**initial_item_groups[0], 'name': 'Updated Name'},
        create_mock_item_group(),
    ]
    parameters = {
        'item_groups': updated_item_groups
    }

    response = catalog.create_or_replace_item_groups(parameters)

    assert response is not None

    stats = response['item_groups']
    expected_stats = {
        'processed': 2,
        'inserted': 1, 
        'updated': 1,
        'deleted': 1
    }

    assert stats == expected_stats

def test_create_or_replace_item_groups_validation():
    '''Should validate item_groups parameter requirements for create_or_replace'''

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

def test_retrieve_item_groups():
    '''Should retrieve all item groups'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    item_groups = [
        create_mock_item_group(),
        create_mock_item_group()
    ]
    parameters = {
        'item_groups': item_groups
    }

    response = catalog.create_item_groups(parameters)

    assert response is not None

    retrieve_response = catalog.retrieve_item_groups()

    assert retrieve_response is not None
    assert 'item_groups' in retrieve_response

    catalog.delete_item_groups()


def test_delete_item_groups():
    '''Should delete all item groups'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    item_groups = [
        create_mock_item_group(),
        create_mock_item_group()
    ]
    parameters = {
        'item_groups': item_groups
    }

    response = catalog.create_item_groups(parameters)

    assert response is not None

    delete_response = catalog.delete_item_groups()

    assert delete_response is not None
    assert 'message' in delete_response
    expected_message = 'We\'ve started deleting all of your groups. This may take some time to complete.'
    assert delete_response['message'] == expected_message


def test_create_or_update_item_groups():
    '''Should create or update item groups'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    initial_item_groups = [
        create_mock_item_group(),
        create_mock_item_group(),
    ]
    parameters = {
        'item_groups': initial_item_groups
    }

    response = catalog.create_item_groups(parameters)

    updated_item_groups = [
        # Keep one existing item group but modify it
        {**initial_item_groups[0], 'name': 'Updated Name'},
        create_mock_item_group(),
    ]
    parameters = {
        'item_groups': updated_item_groups
    }

    response = catalog.create_or_update_item_groups(parameters)

    assert response is not None

    stats = response['item_groups']
    expected_stats = {
        'processed': 2,
        'inserted': 1,
        'updated': 1,
        'deleted': 0
    }

    assert stats == expected_stats

    catalog.delete_item_groups()


def test_create_or_update_item_groups_validation():
    '''Should validate item_groups parameter requirements for create_or_update'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    # Test with missing item_groups parameter
    with raises(
        HttpException,
        match=r'item_groups: none is not an allowed value'
    ):
        catalog.create_or_update_item_groups({})

    # Test with empty item_groups array
    with raises(
        HttpException,
        match=r'item_groups: ensure this value has at least 1 items'
    ):
        catalog.create_or_update_item_groups({'item_groups': []})

    # Test with non-array item_groups
    with raises(
        HttpException,
        match=r'item_groups: value is not a valid list'
    ):
        catalog.create_or_update_item_groups({'item_groups': 'not an array'})
