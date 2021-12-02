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


class Catalog:
    '''Catalog Class'''

    def __init__(self, options):
        self.__options = options or {}

    def replace_catalog(self, parameters=None):
        #pylint: disable=line-too-long
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
        #pylint: disable=line-too-long
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
        #pylint: disable=line-too-long
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
