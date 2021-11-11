'''ConstructorIO Python Client - Recommendations Tests'''

import re
from os import environ
from unittest import mock

import requests
from pytest import raises

from constructorio_python.constructorio import ConstructorIO
from constructorio_python.helpers.exception import HttpException

TEST_API_KEY = environ['TEST_API_KEY']
VALID_CLIENT_ID = '2b23dd74-5672-4379-878c-9182938d2710'
VALID_SESSION_ID = 2
VALID_OPTIONS = { 'api_key': TEST_API_KEY }
POD_ID = 'item_page_1'
POD_ID_QUERY_RECOMMENDATIONS = 'query_recommendations'
POD_ID_FILTERED_ITEMS_RECOMMENDATIONS = 'filtered_items'
ITEM_ID = 'power_drill'
ITEM_IDS = [ITEM_ID, 'drill']

def test_with_valid_pod_id_and_identifiers():
    '''Should return a response with a valid query and client + session identifiers'''

    client_session_identifiers = {
      'client_id': VALID_CLIENT_ID,
      'session_id': VALID_SESSION_ID,
    }
    recommendations = ConstructorIO(VALID_OPTIONS).recommendations
    response = recommendations.get_recommendation_results(POD_ID, client_session_identifiers)

    assert isinstance(response.get('request'), dict)
    assert isinstance(response.get('response'), dict)
    assert isinstance(response.get('result_id'), str)
    assert response.get('request').get('pod_id') == POD_ID