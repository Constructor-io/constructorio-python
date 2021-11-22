
'''ConstructorIO Python Client - Catalog Tests'''

from os import environ
from time import sleep

import pytest
import requests

from constructor_io.constructor_io import ConstructorIO

TEST_API_KEY = environ['TEST_API_KEY']
TEST_API_TOKEN = environ['TEST_API_TOKEN']
VALID_OPTIONS = { 'api_key': TEST_API_KEY, 'api_token': TEST_API_TOKEN }
SECTION = 'Products'
CATALOG_EXAMPLES_BASE_URL = 'https://raw.githubusercontent.com/Constructor-io/integration-examples/main/catalog/' #pylint: disable=line-too-long
ITEMS = requests.get(f'{CATALOG_EXAMPLES_BASE_URL}items.csv').content
VARIATIONS = requests.get(f'{CATALOG_EXAMPLES_BASE_URL}variations.csv').content
ITEM_GROUPS = requests.get(f'{CATALOG_EXAMPLES_BASE_URL}item_groups.csv').content

@pytest.fixture(autouse=True)
def slow_down_tests():
    '''Sleep between tests'''

    yield
    sleep(2)

def test_with_replace_items():
    '''Should replace a catalog of items'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    data = {
        'items': ITEMS,
        'section': SECTION
    }

    catalog.replace_catalog(data)

def test_with_replace_variations():
    '''Should replace a catalog of variations'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    data = {
        'variations': VARIATIONS,
        'section': SECTION
    }

    catalog.replace_catalog(data)

def test_with_replace_item_groups():
    '''Should replace a catalog of item_groups'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    data = {
        'item_groups': ITEM_GROUPS,
        'section': SECTION
    }

    catalog.replace_catalog(data)

def test_with_replace_items_variations_item_groups():
    '''Should replace a catalog of items, variations, and item_groups'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    data = {
        'items': ITEMS,
        'variations': VARIATIONS,
        'item_groups': ITEM_GROUPS,
        'section': SECTION
    }

    catalog.replace_catalog(data)

def test_with_update_items():
    '''Should update a catalog of items'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    data = {
        'items': ITEMS,
        'section': SECTION
    }

    catalog.update_catalog(data)

def test_with_update_variations():
    '''Should update a catalog of variations'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    data = {
        'variations': VARIATIONS,
        'section': SECTION
    }

    catalog.update_catalog(data)

def test_with_update_item_groups():
    '''Should update a catalog of item_groups'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    data = {
        'item_groups': ITEM_GROUPS,
        'section': SECTION
    }

    catalog.update_catalog(data)

def test_with_update_items_variations_item_groups():
    '''Should update a catalog of items, variations, and item_groups'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    data = {
        'items': ITEMS,
        'variations': VARIATIONS,
        'item_groups': ITEM_GROUPS,
        'section': SECTION
    }

    catalog.update_catalog(data)

def test_with_patch_items():
    '''Should patch a catalog of items'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    data = {
        'items': ITEMS,
        'section': SECTION
    }

    catalog.patch_catalog(data)

def test_with_patch_variations():
    '''Should patch a catalog of variations'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    data = {
        'variations': VARIATIONS,
        'section': SECTION
    }

    catalog.patch_catalog(data)

def test_with_patch_item_groups():
    '''Should patch a catalog of item_groups'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    data = {
        'item_groups': ITEM_GROUPS,
        'section': SECTION
    }

    catalog.patch_catalog(data)

def test_with_patch_items_variations_item_groups():
    '''Should patch a catalog of items, variations, and item_groups'''

    catalog = ConstructorIO(VALID_OPTIONS).catalog
    data = {
        'items': ITEMS,
        'variations': VARIATIONS,
        'item_groups': ITEM_GROUPS,
        'section': SECTION
    }

    catalog.patch_catalog(data)
