import time
import requests
import logging

try:
    from urllib.parse import urlencode  # Python 3
except ImportError:
    from urllib import urlencode  # Python 2

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# In seconds. Will increase each iteration
RETRY_TIMEOUT_IN_CASE_OF_SERVER_ERROR = 10


class ConstructorError(Exception):
    def __init__(self, message=""):
        super(ConstructorError, self).__init__(
            "Undefined error with Constructor.io: " + str(message))


class ConstructorInputError(ConstructorError):
    def __init__(self, message=""):
        super(Exception, self).__init__("Bad request: " + str(message))


class ConstructorServerError(ConstructorError):
    def __init__(self, message=""):
        super(Exception, self).__init__("Server error: " + str(message))


class ConstructorIO(object):
    def __init__(self, api_token, key=None, protocol="https",
                 host="ac.cnstrc.com", autocomplete_key=None,
                 server_error_retries=10):

        # Support backward capability after
        # renaming `autocomplete_key` to `key`
        if key is None:
            key = autocomplete_key
        if key is None and autocomplete_key is None:
            raise TypeError("__init__() missing argument 'key'")

        self._api_token = api_token
        self._key = key
        self._protocol = protocol
        self._host = host
        self._server_error_retries = server_error_retries

    def _serialize_params(self, params, sort=False):
        """
        Serialize dictionary in URL's GET format
        :param params: Dictionary for serialization
        :param sort: If reproducible order is required (For tests etc)
        :return: String
        """
        if sort:
            params = sorted(params.items(), key=lambda val: val[0])
        return urlencode(params)

    def _make_url(self, endpoint, params=None):
        if not params:
            params = {}
        params["key"] = self._key
        return "{0}://{1}/{2}?{3}".format(self._protocol, self._host, endpoint,
                                          self._serialize_params(params))

    def __make_server_request(self, request_method, *args, **kwargs):
        retries_left = self._server_error_retries
        timeout = RETRY_TIMEOUT_IN_CASE_OF_SERVER_ERROR

        while True:
            try:
                # Wrap server error codes as exceptions
                response = request_method(*args, **kwargs)
                if response.status_code // 100 == 5:
                    raise ConstructorServerError(response.text)
                elif response.status_code // 100 == 4:
                    raise ConstructorInputError(response.text)
                elif not response.status_code // 100 == 2:
                    raise ConstructorError(response.text)
                return response
            except ConstructorServerError as error:
                # Retry in case of server error
                if retries_left <= 0:
                    raise error
                timeout += RETRY_TIMEOUT_IN_CASE_OF_SERVER_ERROR
                logger.warning('%s Retrying in %d seconds. Retries left: %d',
                               error, timeout, retries_left)
                retries_left -= 1
                time.sleep(timeout)

    def query(self, query_str, *args, **kwargs):
        url = self._make_url("autocomplete/" + query_str)
        resp = self.__make_server_request(requests.get, url, *args, **kwargs)
        return resp.json()

    def verify(self):
        url = self._make_url("v1/verify")
        resp = self.__make_server_request(requests.get,
                                          url,
                                          auth=(self._api_token, ""))
        return resp.json()

    def _add_params_from_kwargs(self, params, **kwargs):
        # The '_force' kwarg just indicates that `force` should be added
        # to the query string, but it shouldn't be in the JSON body of the
        # request
        params.update({k: v for k, v in kwargs.items() if k != '_force'})

    def add(self, item_name, autocomplete_section, **kwargs):
        return self._item_method(
            'Add', requests.post,
            dict(kwargs, item_name=item_name, autocomplete_section=autocomplete_section),
        )

    def add_or_update(self, item_name, autocomplete_section, **kwargs):
        return self._item_method(
            'Add or Update', requests.put,
            dict(kwargs, item_name=item_name, autocomplete_section=autocomplete_section),
            url_params={'force': 1}
        )

    def add_batch(self, items, autocomplete_section, **kwargs):
        return self._item_batch_method(
            'Add Batch', requests.post,
            self._format_items_batch_data(items, autocomplete_section, **kwargs)
        )

    def add_or_update_batch(self, items, autocomplete_section, **kwargs):
        return self._item_batch_method(
            'Add or Update Batch', requests.put,
            self._format_items_batch_data(items, autocomplete_section, **kwargs),
            url_params={"force": 1}
        )

    def remove(self, item_name, autocomplete_section):
        return self._item_method(
            'Remove', requests.delete,
            dict(item_name=item_name, autocomplete_section=autocomplete_section)
        )

    def remove_batch(self, items, autocomplete_section):
        return self._item_batch_method(
            'Remove Batch', requests.delete,
            self._format_items_batch_data(items, autocomplete_section),
        )

    def modify(self, item_name, autocomplete_section, **kwargs):
        return self._item_method(
            'Modify', requests.put,
            dict(kwargs, item_name=item_name, autocomplete_section=autocomplete_section)
        )

    def patch(self, item_name, autocomplete_section, **kwargs):
        return self._item_method(
            'Patch', requests.patch,
            dict(kwargs, item_name=item_name, autocomplete_section=autocomplete_section)
        )

    def patch_batch(self, items, autocomplete_section, **kwargs):
        return self._item_batch_method(
            'Patch Batch', requests.patch,
            self._format_items_batch_data(items, autocomplete_section, **kwargs),
        )

    def track_conversion(self, term, autocomplete_section, **kwargs):
        params = {
            "term": term,
            "autocomplete_section": autocomplete_section,
        }
        if "item" in kwargs:
            params["item"] = kwargs["item"]
        url = self._make_url("v1/conversion")
        if not self._api_token:
            raise IOError("You must have an API token to track conversions!")
        self.__make_server_request(requests.post,
                                   url,
                                   json=params,
                                   auth=(self._api_token, ""))
        return True

    def track_click_through(self, term, autocomplete_section, **kwargs):
        params = {
            "term": term,
            "autocomplete_section": autocomplete_section,
        }
        if "item" in kwargs:
            params["item"] = kwargs["item"]
        if "revenue" in kwargs:
            params["revenue"] = kwargs["revenue"]
        url = self._make_url("v1/click_through")
        if not self._api_token:
            raise IOError(
                "You must have an API token to track click throughs!")
        self.__make_server_request(requests.post,
                                   url,
                                   json=params,
                                   auth=(self._api_token, ""))
        return True

    def track_search(self, term, **kwargs):
        params = {
            "term": term
        }
        if "num_results" in kwargs:
            params["num_results"] = kwargs["num_results"]
        url = self._make_url("v1/search")
        if not self._api_token:
            raise IOError("You must have an API token to track searches!")
        self.__make_server_request(requests.post,
                                   url,
                                   json=params,
                                   auth=(self._api_token, ""))
        return True

    def _item_method(self, method_name, request_method, data, url_params=None):
        return self._non_retrieve_method(
            method_name=method_name, method_url="v1/item", request_method=request_method,
            data=data, url_params=url_params
        )

    def _item_batch_method(self, method_name, request_method, data, url_params=None):
        return self._non_retrieve_method(
            method_name=method_name, method_url="v1/batch_items", request_method=request_method,
            data=data, url_params=url_params
        )

    def _format_items_batch_data(self, items, autocomplete_section, **kwargs):
        for item in items:
            self._add_params_from_kwargs(item, **kwargs)
        return {"items": items, "autocomplete_section": autocomplete_section}

    def _non_retrieve_method(self, method_name, method_url, request_method, data,
                             url_params=None):
        """Process POST, PUT, PATCH, DELETE methods"""
        if not self._api_token:
            raise IOError(
                "You must have an API token to use the %s method!" % method_name)

        url = self._make_url(method_url, url_params or {})
        self.__make_server_request(request_method,
                                   url,
                                   json=data,
                                   auth=(self._api_token, ""))
        return True