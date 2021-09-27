'''ConstructorIO Python Client - Autocomplete Tests'''

from os import environ

from constructorio_python.constructorio import ConstructorIO

test_api_key = environ['TEST_API_KEY']
valid_client_id = '2b23dd74-5672-4379-878c-9182938d2710'
valid_session_id = 2
valid_options = { 'api_key': test_api_key }

class TestAutocomplete():
    '''ConstructorIO - Autocomplete'''

    def test_get_autocomplete_results(self):
        client_session_identifiers = {
            'client_id': valid_client_id,
            'session_id': valid_session_id,
        }
        query = 'item'
        autocomplete = ConstructorIO(valid_options).autocomplete
        response = autocomplete.get_autocomplete_results(query, {}, {**client_session_identifiers})

