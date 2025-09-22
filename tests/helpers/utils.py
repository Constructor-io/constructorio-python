'''Test Utils'''

import uuid


def create_mock_item():
    '''Creates a mock item to be used in Items API tests'''
    item_id = str(uuid.uuid1())
    name = 'Product ' + item_id
    url = 'https://constructor.io/products/' + item_id
    facets = { 'color': ['blue', 'red'] }
    data = {
        'facets': facets,
        'brand': 'abc',
        'url': url,
        'image_url': url,
        'complexMetadataField': {
            'key1': 'val1',
            'key2': 'val2',
        }
    }
    item = {
        'id': item_id,
        'name': name,
        'data': data,
    }

    return item

def create_mock_variation(item_id=None):
    '''Creates a mock variation to be used in Items API tests'''
    variation_id = str(uuid.uuid1())
    name = 'Variation ' + variation_id
    url = 'https://constructor.io/products/' + variation_id
    facets = { 'color': ['blue', 'red'] }
    data = {
        'facets': facets,
        'brand': 'abc',
        'url': url,
        'image_url': url,
        'complexMetadataField': {
            'key1': 'val1',
            'key2': 'val2',
        }
    }
    variation = {
        'id': variation_id,
        'item_id': item_id,
        'name': name,
        'data': data,
    }

    return variation

def create_mock_item_group():
    '''Creates a mock item group to be used in Item Groups API tests'''
    item_group_id = str(uuid.uuid4())
    name = 'Item Group ' + item_group_id
    data = {
        'complexMetadataField': {
            'key1': 'val1',
            'key2': 'val2',
        }
    }
    item_group = {
        'id': item_group_id,
        'name': name,
        'data': data,
        'parent_ids': []
    }

    return item_group
