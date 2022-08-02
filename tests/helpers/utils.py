import uuid


def create_mock_item():
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
