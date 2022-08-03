'''ConstructorIO Python Client - Items Catalog Tests'''

from os import environ
from time import sleep

import pytest
import requests
from pytest import raises

from constructor_io.constructor_io import ConstructorIO
from constructor_io.helpers.exception import HttpException
from tests.helpers.utils import create_mock_item, create_mock_variation

TEST_API_KEY = environ['TEST_API_KEY']
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

def test_with_add_or_update_items():
    '''Should add or update items'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    items = [
        create_mock_item(),
        create_mock_item(),
    ]
    parameters = {
        'items': items,
    }

    response = catalog.add_or_update_items(parameters)
    items_to_clean_up.extend(items)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_add_or_update_items_using_all_parameters():
    '''Should add or update items using all parameters'''

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

    response = catalog.add_or_update_items(parameters)
    items_to_clean_up.extend(items)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_modify_items():
    '''Should modify items'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    item_old = create_mock_item()
    items_old = [ item_old ]
    parameters_old = {
        'items': items_old,
    }

    response_old = catalog.add_or_update_items(parameters_old)

    item_new = item_old
    item_new['name'] = 'Updated Item Name'
    items_new = [ item_new ]
    parameters_new = {
        'items': items_new,
    }

    response_new = catalog.modify_items(parameters_new)
    items_to_clean_up.extend(items_new)

    assert isinstance(response_new.get('task_id'), int)
    assert isinstance(response_new.get('task_status_path'), str)

def test_with_modify_items_using_all_parameters():
    '''Should modify items using all parameters'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    item_old = create_mock_item()
    items_old = [ item_old ]
    parameters_old = {
        'items': items_old,
    }

    response_old = catalog.add_or_update_items(parameters_old)

    item_new = item_old
    item_new['name'] = 'Updated Item Name'
    items_new = [ item_new ]
    parameters_new = {
        'items': items_new,
        'section': 'Products',
        'notification_email': 'test@constructor.io',
        'force': True,
    }

    response_new = catalog.modify_items(parameters_new)
    items_to_clean_up.extend(items_new)

    assert isinstance(response_new.get('task_id'), int)
    assert isinstance(response_new.get('task_status_path'), str)

def test_with_remove_items():
    '''Should remove items'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    items = [
        create_mock_item(),
        create_mock_item(),
    ]
    parameters_for_add = {
        'items': items,
    }

    catalog.add_or_update_items(parameters_for_add)

    items.extend(items_to_clean_up)

    # Remove duplicates from items list
    unique_items = []
    [unique_items.append(x) for x in items if x not in unique_items]

    parameters = {
        'items': unique_items,
    }

    response = catalog.remove_items(parameters)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_remove_items_using_all_parameters():
    '''Should remove items using all parameters'''

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

    catalog.add_or_update_items(parameters)
    response = catalog.remove_items(parameters)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_get_items():
    '''Should get items'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.get_items()

    assert isinstance(response.get('items'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') >= 1

def test_with_get_items_using_single_id():
    '''Should get items using single id'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.get_items({ 'ids': ['10001'] })

    assert isinstance(response.get('items'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') >= 1

def test_with_get_items_using_multiple_ids():
    '''Should get items using multiple ids'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.get_items({ 'ids': ['10001', '10002'] })

    assert isinstance(response.get('items'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') >= 1

def test_with_get_items_using_all_parameters():
    '''Should get items using all parameters'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.get_items({ 
        'section': 'Products',
        'num_results_per_page': 2,
        'page': 2,
    })

    assert isinstance(response.get('items'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') >= 1

def test_with_add_or_update_variations():
    '''Should add or update variations'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    variations = [
        create_mock_variation('random-id'),
        create_mock_variation('random-id'),
    ]
    parameters = {
        'variations': variations,
    }

    response = catalog.add_or_update_variations(parameters)
    variations_to_clean_up.extend(variations)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_add_or_update_variations_using_all_parameters():
    '''Should add or update variations using all parameters'''

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

    response = catalog.add_or_update_variations(parameters)
    variations_to_clean_up.extend(variations)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_modify_variations():
    '''Should modify variations'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    variation_old = create_mock_variation('random-id')
    variations_old = [ variation_old ]
    parameters_old = {
        'variations': variations_old,
    }

    response_old = catalog.add_or_update_variations(parameters_old)

    variation_new = variation_old
    variation_new['name'] = 'Updated variation Name'
    variations_new = [ variation_new ]
    parameters_new = {
        'variations': variations_new,
    }

    response_new = catalog.modify_variations(parameters_new)
    variations_to_clean_up.extend(variations_new)

    assert isinstance(response_new.get('task_id'), int)
    assert isinstance(response_new.get('task_status_path'), str)

def test_with_modify_variations_without_item_id():
    '''Should modify variations'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    variation_old = create_mock_variation('random-id')
    variations_old = [ variation_old ]
    parameters_old = {
        'variations': variations_old,
    }

    response_old = catalog.add_or_update_variations(parameters_old)

    variation_new = variation_old
    variation_new['name'] = 'Updated variation Name'
    variation_new.pop('item_id')
    variations_new = [ variation_new ]
    parameters_new = {
        'variations': variations_new,
    }

    response_new = catalog.modify_variations(parameters_new)
    variations_to_clean_up.extend(variations_new)

    assert isinstance(response_new.get('task_id'), int)
    assert isinstance(response_new.get('task_status_path'), str)

def test_with_modify_variations_using_all_parameters():
    '''Should modify variations using all parameters'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    variation_old = create_mock_variation('random-id')
    variations_old = [ variation_old ]
    parameters_old = {
        'variations': variations_old,
    }

    response_old = catalog.add_or_update_variations(parameters_old)

    variation_new = variation_old
    variation_new['name'] = 'Updated variation Name'
    variations_new = [ variation_new ]
    parameters_new = {
        'variations': variations_new,
        'section': 'Products',
        'notification_email': 'test@constructor.io',
        'force': True,
    }

    response_new = catalog.modify_variations(parameters_new)
    variations_to_clean_up.extend(variations_new)

    assert isinstance(response_new.get('task_id'), int)
    assert isinstance(response_new.get('task_status_path'), str)

def test_with_remove_variations():
    '''Should remove variations'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    variations = [
        create_mock_variation('random-id'),
        create_mock_variation('random-id'),
    ]
    parameters_for_add = {
        'variations': variations,
    }

    catalog.add_or_update_variations(parameters_for_add)
    variations.extend(variations_to_clean_up)

    # Remove duplicates from the variations list
    unique_variations = []
    [unique_variations.append(x) for x in variations if x not in unique_variations]

    parameters = {
        'variations': unique_variations,
    }

    response = catalog.remove_variations(parameters)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_remove_variations_using_all_parameters():
    '''Should remove variations using all parameters'''

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

    catalog.add_or_update_variations(parameters)
    response = catalog.remove_variations(parameters)

    assert isinstance(response.get('task_id'), int)
    assert isinstance(response.get('task_status_path'), str)

def test_with_get_variations():
    '''Should get variations'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.get_variations()

    assert isinstance(response.get('variations'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') >= 1

def test_with_get_variations_using_single_id():
    '''Should get variations using single id'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.get_variations({ 'ids': ['10001'] })

    assert isinstance(response.get('variations'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') >= 1

def test_with_get_variations_using_multiple_ids():
    '''Should get variations using multiple ids'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.get_variations({ 'ids': ['10001', '10002'] })

    assert isinstance(response.get('variations'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') >= 1

def test_with_get_variations_using_all_parameters():
    '''Should get variations using all parameters'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog

    response = catalog.get_variations({ 
        'section': 'Products',
        'num_results_per_page': 2,
        'page': 2,
    })

    assert isinstance(response.get('variations'), list)
    assert isinstance(response.get('total_count'), int)
    assert response.get('total_count') >= 1
