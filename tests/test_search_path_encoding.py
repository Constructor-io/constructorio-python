from unittest.mock import Mock
from urllib.parse import urlsplit

import pytest

from constructor_io.constructor_io import ConstructorIO


@pytest.mark.parametrize(
    ('method_name', 'response', 'prefix'),
    [
        ('search', {'response': {'results': []}}, '/search/'),
        ('autocomplete', {'sections': {'Products': []}}, '/autocomplete/'),
    ],
)
def test_query_is_encoded_as_one_path_segment(method_name, response, prefix):
    requests = Mock()
    requests.get.return_value.ok = True
    requests.get.return_value.json.return_value = response
    client = ConstructorIO({'api_key': 'test', 'requests': requests})
    method = getattr(getattr(client, method_name), f'get_{method_name}_results')

    method('shirts/a?b')

    url = requests.get.call_args.args[0]
    assert urlsplit(url).path == prefix + 'shirts%2Fa%3Fb'
