'''ConstructorIO Python Client - Items Catalog Tests'''

from os import environ
from time import sleep

import pytest
from pytest import raises

from constructor_io.constructor_io import ConstructorIO
from constructor_io.helpers.exception import HttpException
from tests.helpers.utils import create_mock_item, create_mock_variation

TEST_API_KEY = environ['TEST_CATALOG_API_KEY']
TEST_API_TOKEN = environ['TEST_API_TOKEN']
VALID_OPTIONS = { 'api_key': TEST_API_KEY, 'api_token': TEST_API_TOKEN }
SECTION = 'Products'
items_to_clean_up = []
variations_to_clean_up = []

@pytest.fixture(autouse=True)
def slow_down_tests():
    '''Sleep between tests'''

    yield
    sleep(1)

def test_with_create_or_replace_items():
    '''Should create or replace items'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    items = [
        create_mock_item(),
        create_mock_item(),
    ]
    parameters = {
        'items': items,
    }

    response = catalog.create_or_replace_items(parameters)
    items_to_clean_up.extend(items)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_create_or_replace_items_using_all_parameters():
    '''Should create or replace items using all parameters'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    items = [
        create_mock_item(),
        create_mock_item(),
    ]
    parameters = {
        'items': items,
        'section': 'Products',
        'notification_email': 'test@constructor.io',
        'force': True,
    }

    response = catalog.create_or_replace_items(parameters)
    items_to_clean_up.extend(items)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_create_or_replace_items_no_items():
    '''Should raise an HTTP error'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    with raises(
        HttpException,
        match=r'items must be a list'
    ):
        catalog.create_or_replace_items({})

def test_with_update_items():
    '''Should update items'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    item_old = create_mock_item()
    items_old = [ item_old ]
    parameters_old = {
        'items': items_old,
    }

    catalog.create_or_replace_items(parameters_old)

    item_new = item_old
    item_new['name'] = 'Updated Item Name'
    items_new = [ item_new ]
    parameters_new = {
        'items': items_new,
    }

    response_new = catalog.update_items(parameters_new)
    items_to_clean_up.extend(items_new)

    assert isinstance(response_new.get('task_id'), int)
    assert isinstance(response_new.get('task_status_path'), str)

def test_with_update_items_using_all_parameters():
    '''Should update items using all parameters'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    item_old = create_mock_item()
    items_old = [ item_old ]
    parameters_old = {
        'items': items_old,
    }

    catalog.create_or_replace_items(parameters_old)

    item_new = item_old
    item_new['name'] = 'Updated Item Name'
    items_new = [ item_new ]
    parameters_new = {
        'items': items_new,
        'section': 'Products',
        'notification_email': 'test@constructor.io',
        'force': True,
    }

    response_new = catalog.update_items(parameters_new)
    items_to_clean_up.extend(items_new)

    assert isinstance(response_new.get('task_id'), int)
    assert isinstance(response_new.get('task_status_path'), str)

def test_with_update_items_no_items():
    '''Should raise an HTTP error'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    with raises(
        HttpException,
        match=r'items must be a list'
    ):
        catalog.update_items({})

def test_with_delete_items():
    '''Should delete items'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    items = [
        create_mock_item(),
        create_mock_item(),
    ]
    parameters_for_add = {
        'items': items,
    }

    catalog.create_or_replace_items(parameters_for_add)

    items.extend(items_to_clean_up)

    # Remove duplicates from items list
    unique_items = []
    [unique_items.append(x) for x in items if x not in unique_items] # pylint: disable=expression-not-assigned

    parameters = {
        'items': unique_items,
    }

    response = catalog.delete_items(parameters)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_delete_items_using_all_parameters():
    '''Should delete items using all parameters'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    items = [
        create_mock_item(),
        create_mock_item(),
    ]
    parameters = {
        'items': items,
        'section': 'Products',
        'notification_email': 'test@constructor.io',
        'force': True,
    }

    catalog.create_or_replace_items(parameters)
    response = catalog.delete_items(parameters)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_retrieve_items():
    '''Should retrieve items'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.retrieve_items()

    assert isinstance(response.get('items'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') >= 1

def test_with_retrieve_items_using_single_id():
    '''Should retrieve items using single id'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.retrieve_items({ 'ids': ['10001'] })

    assert isinstance(response.get('items'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') == 1

def test_with_retrieve_items_using_multiple_ids():
    '''Should retrieve items using multiple ids'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.retrieve_items({ 'ids': ['10001', '10002'] })

    assert isinstance(response.get('items'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') == 2

def test_with_retrieve_items_using_all_parameters():
    '''Should retrieve items using all parameters'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.retrieve_items({
        'section': 'Products',
        'num_results_per_page': 2,
        'page': 2,
    })

    assert isinstance(response.get('items'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') >= 1

def test_with_create_or_replace_variations():
    '''Should create or replace variations'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    variations = [
        create_mock_variation('random-id'),
        create_mock_variation('random-id'),
    ]
    parameters = {
        'variations': variations,
    }

    response = catalog.create_or_replace_variations(parameters)
    variations_to_clean_up.extend(variations)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_create_or_replace_variations_using_all_parameters():
    '''Should create or replace variations using all parameters'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    variations = [
        create_mock_variation('random-id'),
        create_mock_variation('random-id'),
    ]
    parameters = {
        'variations': variations,
        'section': 'Products',
        'notification_email': 'test@constructor.io',
        'force': True,
    }

    response = catalog.create_or_replace_variations(parameters)
    variations_to_clean_up.extend(variations)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_create_or_replace_variations_no_variations():
    '''Should raise an HTTP error'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    with raises(
        HttpException,
        match=r'variations must be a list'
    ):
        catalog.create_or_replace_variations({})

def test_with_update_variations():
    '''Should update variations'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    variation_old = create_mock_variation('random-id')
    variations_old = [ variation_old ]
    parameters_old = {
        'variations': variations_old,
    }

    catalog.create_or_replace_variations(parameters_old)

    variation_new = variation_old
    variation_new['name'] = 'Updated variation Name'
    variations_new = [ variation_new ]
    parameters_new = {
        'variations': variations_new,
    }

    response_new = catalog.update_variations(parameters_new)
    variations_to_clean_up.extend(variations_new)

    assert isinstance(response_new.get('task_id'), int)
    assert isinstance(response_new.get('task_status_path'), str)

def test_with_update_variations_without_item_id():
    '''Should update variations'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    variation_old = create_mock_variation('random-id')
    variations_old = [ variation_old ]
    parameters_old = {
        'variations': variations_old,
    }

    catalog.create_or_replace_variations(parameters_old)

    variation_new = variation_old
    variation_new['name'] = 'Updated variation Name'
    variation_new.pop('item_id')
    variations_new = [ variation_new ]
    parameters_new = {
        'variations': variations_new,
    }

    response_new = catalog.update_variations(parameters_new)
    variations_to_clean_up.extend(variations_new)

    assert isinstance(response_new.get('task_id'), int)
    assert isinstance(response_new.get('task_status_path'), str)

def test_with_update_variations_using_all_parameters():
    '''Should update variations using all parameters'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    variation_old = create_mock_variation('random-id')
    variations_old = [ variation_old ]
    parameters_old = {
        'variations': variations_old,
    }

    catalog.create_or_replace_variations(parameters_old)

    variation_new = variation_old
    variation_new['name'] = 'Updated variation Name'
    variations_new = [ variation_new ]
    parameters_new = {
        'variations': variations_new,
        'section': 'Products',
        'notification_email': 'test@constructor.io',
        'force': True,
    }

    response_new = catalog.update_variations(parameters_new)
    variations_to_clean_up.extend(variations_new)

    assert isinstance(response_new.get('task_id'), int)
    assert isinstance(response_new.get('task_status_path'), str)

def test_with_update_variations_no_variations():
    '''Should raise an HTTP error'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    with raises(
        HttpException,
        match=r'variations must be a list'
    ):
        catalog.update_variations({})

def test_with_delete_variations():
    '''Should delete variations'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    variations = [
        create_mock_variation('random-id'),
        create_mock_variation('random-id'),
    ]
    parameters_for_add = {
        'variations': variations,
    }

    catalog.create_or_replace_variations(parameters_for_add)
    variations.extend(variations_to_clean_up)

    # Remove duplicates from the variations list
    unique_variations = []
    [unique_variations.append(x) for x in variations if x not in unique_variations] # pylint: disable=expression-not-assigned

    parameters = {
        'variations': unique_variations,
    }

    response = catalog.delete_variations(parameters)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_delete_variations_using_all_parameters():
    '''Should delete variations using all parameters'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    variations = [
        create_mock_variation('random-id'),
        create_mock_variation('random-id'),
    ]
    parameters = {
        'variations': variations,
        'section': 'Products',
        'notification_email': 'test@constructor.io',
        'force': True,
    }

    catalog.create_or_replace_variations(parameters)
    response = catalog.delete_variations(parameters)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_retrieve_variations():
    '''Should retrieve variations'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.retrieve_variations()

    assert isinstance(response.get('variations'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') >= 1

def test_with_retrieve_variations_using_single_id():
    '''Should retrieve variations using single id'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.retrieve_variations({ 'ids': ['20001'] })

    assert isinstance(response.get('variations'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') == 1

def test_with_retrieve_variations_using_multiple_ids():
    '''Should retrieve variations using multiple ids'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.retrieve_variations({ 'ids': ['20001', 'M0E20000000E2ZJ'] })

    assert isinstance(response.get('variations'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') == 2

def test_with_retrieve_variations_using_item_id():
    '''Should retrieve variations using item id'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.retrieve_variations({ 'item_id': '10001' })

    assert isinstance(response.get('variations'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') == 1

def test_with_retrieve_variations_using_all_parameters():
    '''Should retrieve variations using all parameters'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.retrieve_variations({
        'section': 'Products',
        'num_results_per_page': 2,
        'page': 2,
    })

    assert isinstance(response.get('variations'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') >= 1
