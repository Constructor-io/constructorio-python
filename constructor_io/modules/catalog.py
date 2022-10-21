'''Catalog Module'''

from urllib.parse import quote, urlencode

import requests as r

from constructor_io.helpers.exception import ConstructorException
from constructor_io.helpers.utils import (clean_params, create_auth_header,
                                          create_request_headers,
                                          throw_http_exception_from_response)


def _create_query_params_and_file_data(parameters):
    '''Create query params and file data'''

    query_params = {}
    file_data = {}

    if parameters:
        section = parameters.get('section')
        notification_email = parameters.get('notification_email')
        force = parameters.get('force')
        items = parameters.get('items')
        variations = parameters.get('variations')
        item_groups = parameters.get('item_groups')

        if section:
            query_params['section'] = section

        if notification_email:
            query_params['notification_email'] = notification_email

        if force:
            query_params['force'] = force

        if items:
            file_data['items'] = ('items.csv', items)

        if variations:
            file_data['variations'] = ('variations.csv', variations)

        if item_groups:
            file_data['item_groups'] = ('item_groups.csv', item_groups)

    return query_params, file_data

def _create_query_params_for_items(parameters):
    '''Create query params for items API (includes variations)'''

    query_params = {}

    if parameters:
        section = parameters.get('section')
        notification_email = parameters.get('notification_email')
        force = parameters.get('force')
        num_results_per_page = parameters.get('num_results_per_page')
        page = parameters.get('page')
        ids = parameters.get('ids')

        if ids:
            query_params['id'] = ids

        if section:
            query_params['section'] = section

        if notification_email:
            query_params['notification_email'] = notification_email

        if force:
            query_params['force'] = force

        if num_results_per_page:
            query_params['num_results_per_page'] = num_results_per_page

        if page:
            query_params['page'] = page

    return query_params

def _create_catalog_url(path, options, additional_query_params):
    '''Create catalog API url'''

    api_key = options.get('api_key')
    query_params = {**additional_query_params}

    if not path or not isinstance(path, str):
        raise ConstructorException('path is a required parameter of type string')

    query_params['key'] = api_key
    query_params = clean_params(query_params)
    query_string = urlencode(query_params, doseq=True)

    return f'{options.get("service_url")}/v1/{quote(path)}?{query_string}'

def _create_items_url(path, options, additional_query_params):
    '''Create items API url'''

    api_key = options.get('api_key')
    version = options.get('version')
    query_params = {**additional_query_params}

    if not path or not isinstance(path, str):
        raise ConstructorException('path is a required parameter of type string')

    query_params['key'] = api_key
    query_params['c'] = version
    query_params = clean_params(query_params)
    query_string = urlencode(query_params, doseq=True)

    return f'{options.get("service_url")}/v2/{quote(path)}?{query_string}'


class Catalog:
    '''Catalog Class'''

    def __init__(self, options):
        self.__options = options or {}

    def replace_catalog(self, parameters=None):
        '''
        Send full catalog files to replace the current catalog

        :param dict parameters: Additional parameters for catalog details
        :param str parameters.section: The section to update
        :param str parameters.notification_email: An email address to receive an email notification if the task fails
        :param bool parameters.force: Process the catalog even if it will invalidate a large number of existing items
        :param file parameters.items: The CSV file with all new items
        :param file parameters.variations: The CSV file with all new variations
        :param file parameters.item_groups: The CSV file with all new item_groups
        '''

        query_params, file_data = _create_query_params_and_file_data(parameters)
        request_url = _create_catalog_url('catalog', self.__options, query_params)
        requests = self.__options.get('requests') or r

        response = requests.put(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options),
            files=file_data
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        return json

    def update_catalog(self, parameters=None):
        '''
        Send full catalog files to update the current catalog

        :param dict parameters: Additional parameters for catalog details
        :param str parameters.section: The section to update
        :param str parameters.notification_email: An email address to receive an email notification if the task fails
        :param bool parameters.force: Process the catalog even if it will invalidate a large number of existing items
        :param file parameters.items: The CSV file with all new items
        :param file parameters.variations: The CSV file with all new variations
        :param file parameters.item_groups: The CSV file with all new item_groups
        '''

        query_params, file_data = _create_query_params_and_file_data(parameters)
        request_url = _create_catalog_url('catalog', self.__options, query_params)
        requests = self.__options.get('requests') or r

        response = requests.patch(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options),
            files=file_data
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        return json

    def patch_catalog(self, parameters=None):
        '''
        Send full catalog files to update the current catalog

        :param dict parameters: Additional parameters for catalog details
        :param str parameters.section: The section to update
        :param str parameters.notification_email: An email address to receive an email notification if the task fails
        :param bool parameters.force: Process the catalog even if it will invalidate a large number of existing items
        :param file parameters.items: The CSV file with all new items
        :param file parameters.variations: The CSV file with all new variations
        :param file parameters.item_groups: The CSV file with all new item_groups
        '''

        query_params, file_data = _create_query_params_and_file_data(parameters)
        request_url = _create_catalog_url('catalog', self.__options, { **query_params, 'patch_delta': True })
        requests = self.__options.get('requests') or r

        response = requests.patch(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options),
            files=file_data
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        return json

    def create_or_replace_items(self, parameters=None):
        '''
        Add multiple items to index whilst replacing existing ones (limit of 1,000)

        :param list parameters.items: A list of items with the same attributes as defined in https://docs.constructor.io/rest_api/items/items/#item-schema
        :param str parameters.section: The section to update
        :param str parameters.notification_email: An email address to receive an email notification if the task fails
        :param bool parameters.force: Process the update even if it will invalidate a large number of existing items
        '''

        query_params = _create_query_params_for_items(parameters)
        request_url = _create_items_url('items', self.__options, query_params)
        requests = self.__options.get('requests') or r

        response = requests.put(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options),
            json={ 'items': parameters.get('items') }
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        return json

    def update_items(self, parameters=None):
        '''
        Update multiple items in the index (limit of 1,000)

        :param list parameters.items: A list of items with the same attributes as defined in https://docs.constructor.io/rest_api/items/items/#item-schema
        :param str parameters.section: The section to update
        :param str parameters.notification_email: An email address to receive an email notification if the task fails
        :param bool parameters.force: Process the update even if it will invalidate a large number of existing items
        '''

        query_params = _create_query_params_for_items(parameters)
        request_url = _create_items_url('items', self.__options, query_params)
        requests = self.__options.get('requests') or r

        response = requests.patch(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options),
            json={ 'items': parameters.get('items') }
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        return json

    def delete_items(self, parameters=None):
        '''
        Delete multiple items from the index (limit of 1,000)

        :param list parameters.items: A list of items with the same attributes as defined in https://docs.constructor.io/rest_api/items/items/#item-schema (only IDs are required)
        :param str parameters.section: The section to update
        :param str parameters.notification_email: An email address to receive an email notification if the task fails
        :param bool parameters.force: Process the update even if it will invalidate a large number of existing items
        '''

        query_params = _create_query_params_for_items(parameters)
        request_url = _create_items_url('items', self.__options, query_params)
        requests = self.__options.get('requests') or r
        items = parameters.get('items') or []
        items_with_only_ids = list(map(lambda x: { 'id': x.get('id') }, items))

        response = requests.delete(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options),
            json={ 'items': items_with_only_ids }
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        return json

    def retrieve_items(self, parameters=None):
        '''
        Retrieves multiple items from the index (limit of 1,000)

        :param list parameters.ids: A list of item IDs to retrieve
        :param str parameters.section: The section to retrieve from
        :param int parameters.num_results_per_page: The number of items to return. Defaults to 100. Maximum value 100
        :param int parameters.page: The page of results to return. Defaults to 1
        '''

        if not parameters:
            parameters = {}

        query_params = _create_query_params_for_items(parameters)

        request_url = _create_items_url('items', self.__options, query_params)
        requests = self.__options.get('requests') or r

        response = requests.get(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options),
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        return json

    def create_or_replace_variations(self, parameters=None):
        '''
        Add multiple variations to index whilst replacing existing ones (limit of 1,000)

        :param list parameters.variations: A list of variations with the same attributes as defined in https://docs.constructor.io/rest_api/variations/variations/#item-schema
        :param str parameters.section: The section to update
        :param str parameters.notification_email: An email address to receive an email notification if the task fails
        :param bool parameters.force: Process the update even if it will invalidate a large number of existing variations
        '''

        query_params = _create_query_params_for_items(parameters)
        request_url = _create_items_url('variations', self.__options, query_params)
        requests = self.__options.get('requests') or r

        response = requests.put(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options),
            json={ 'variations': parameters.get('variations') }
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        return json

    def update_variations(self, parameters=None):
        '''
        Update multiple variations in the index (limit of 1,000)

        :param list parameters.variations: A list of variations with the same attributes as defined in https://docs.constructor.io/rest_api/variations/variations/#item-schema
        :param str parameters.section: The section to update
        :param str parameters.notification_email: An email address to receive an email notification if the task fails
        :param bool parameters.force: Process the update even if it will invalidate a large number of existing variations
        '''

        query_params = _create_query_params_for_items(parameters)
        request_url = _create_items_url('variations', self.__options, query_params)
        requests = self.__options.get('requests') or r

        response = requests.patch(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options),
            json={ 'variations': parameters.get('variations') }
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        return json

    def delete_variations(self, parameters=None):
        '''
        Delete multiple variations from the index (limit of 1,000)

        :param list parameters.variations: A list of variations with the same attributes as defined in https://docs.constructor.io/rest_api/variations/variations/#item-schema (only IDs are required)
        :param str parameters.section: The section to update
        :param str parameters.notification_email: An email address to receive an email notification if the task fails
        :param bool parameters.force: Process the update even if it will invalidate a large number of existing variations
        '''

        query_params = _create_query_params_for_items(parameters)
        request_url = _create_items_url('variations', self.__options, query_params)
        requests = self.__options.get('requests') or r
        variations = parameters.get('variations') or []
        variations_with_only_ids = list(map(lambda x: { 'id': x.get('id') }, variations))

        response = requests.delete(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options),
            json={ 'variations': variations_with_only_ids }
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        return json

    def retrieve_variations(self, parameters=None):
        '''
        Retrieves multiple variations from the index (limit of 1,000)

        :param list parameters.ids: A list of variation IDs to retrieve
        :param str parameters.item_id: Item ID of variations to retrieve
        :param str parameters.section: The section to retrieve from
        :param int parameters.num_results_per_page: The number of variations to return. Defaults to 100. Maximum value 100
        :param int parameters.page: The page of results to return. Defaults to 1
        '''

        if not parameters:
            parameters = {}

        query_params = _create_query_params_for_items(parameters)
        item_id = parameters.get('item_id')

        if item_id:
            query_params['item_id'] = item_id

        request_url = _create_items_url('variations', self.__options, query_params)
        requests = self.__options.get('requests') or r

        response = requests.get(
            request_url,
            auth=create_auth_header(self.__options),
            headers=create_request_headers(self.__options),
        )

        if not response.ok:
            throw_http_exception_from_response(response)

        json = response.json()

        return json
