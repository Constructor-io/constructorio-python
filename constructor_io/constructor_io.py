import requests
import urllib

class ConstructorError(Exception):
    pass

class ConstructorIO(object):
    def __init__(self, api_token, autocomplete_key, protocol="https",
                 host="ac.cnstrc.com"):
        """
        If you use HTTPS, you need a different version of requests
        """
        self._api_token = api_token
        self._autocomplete_key = autocomplete_key
        self._protocol = protocol
        self._host = host

    def _serialize_params(self, params):
        return urllib.urlencode(params)

    def _make_url(self, endpoint, params=None):
        if not params:
            params = {}
        params["autocomplete_key"] = self._autocomplete_key
        return "{0}://{1}/{2}?{3}".format(self._protocol, self._host, endpoint,
                                          self._serialize_params(params))

    def query(self, query_str):
        url = self._make_url("autocomplete/" + query_str)
        resp = requests.get(url)
        if resp.status_code != 200:
            raise ConstructorError(resp.text)
        else:
            return resp.json()

    def verify(self):
        url = self._make_url("v1/verify")
        resp = requests.get(
            url,
            auth=(self._api_token, "")
        )
        if resp.status_code != 200:
            raise ConstructorError(resp.text)
        else:
            return resp.json()

    def update_params_with_kwargs(self, params, kwargs):
        """
        Adds all the key-value pairs from **kwargs into params, if and only
        if the keys in **kwargs belong to a set of pre-defined keys.

        Dictionaries are passed by reference, so the params dict is modified.

        :param params: A dict that contains the keys "item_name" and "autocomplete_section"
        :param kwargs: A dict with keys that needs to be merged into params
        :return: None
        """
        print kwargs.items()
        keys = ["suggested_score", "keywords", "description", "url",
                "image_url"]
        params.update({k: v for k, v in kwargs.iteritems() if k in keys})

    def check_for_non_default_keys(self, kwargs):
        permitted_keys = ["item_name", "autocomplete_section",
                          "suggested_score", "keywords", "url", "image_url",
                          "description", "id"]
        for k in kwargs.iterkeys():
            if k not in permitted_keys:
                raise IOError(
                    "You have submitted an invalid key in the keyword arguments.")

    def add_metadata_to_params(self, params, metadata):
        if metadata:
            params.update(metadata)

    def add(self, item_name, autocomplete_section, metadata=None, **kwargs):
        """
        Adds an autocomplete item. Accepts a metadata dictionary. The keyword
        arguments can only be parameters that exist in the API.

        :param item_name: Name of the item to be added
        :param autocomplete_section: The section that the item is to be added to
        :param kwargs: A dictionary of keys and values
        :param metadata: A dictionary of keys and values to be associated with
        the item, but where the keys are user-defined
        :return: ConstructorError if adding fails, True if adding succeeds
        """
        if not self._api_token:
            raise IOError("You must have an API token to use the Add method!")
        self.check_for_non_default_keys(kwargs)
        params = {"item_name": item_name,
                  "autocomplete_section": autocomplete_section}
        url_params = {}
        self.update_params_with_kwargs(params, kwargs)
        self.add_metadata_to_params(params, metadata)
        request_method = getattr(requests, 'post')
        # force is used to do an add_or_update
        if kwargs.get("_force", 0) == 1:
            url_params["force"] = 1
            request_method = getattr(requests, 'put')
        url = self._make_url("v1/item", url_params)
        resp = request_method(
            url,
            json=params,
            auth=(self._api_token, "")
        )
        if resp.status_code != 204:
            raise ConstructorError(resp.text)
        else:
            return True

    def add_or_update(self, item_name, autocomplete_section, **kwargs):
        if not self._api_token:
            raise IOError(
                "You must have an API token to use the Add or Update method!")
        kwargs["_force"] = 1
        return self.add(item_name, autocomplete_section, **kwargs)

    def add_batch(self, items, autocomplete_section, metadata=None, **kwargs):
        if not self._api_token:
            raise IOError(
                "You must have an API token to use the Add Batch method!")
        self.check_for_non_default_keys(kwargs)
        for item in items:
            self.check_for_non_default_keys(item)
            self.add_metadata_to_params(item, metadata)
            self.update_params_with_kwargs(item, kwargs)
        request_method = getattr(requests, 'post')
        url_params = {}
        # force is used to denote an add_or_update
        if kwargs.get("_force", 0) == 1:
            url_params["force"] = 1
            request_method = getattr(requests, 'put')
        params = {"items": items, "autocomplete_section": autocomplete_section}
        url = self._make_url("v1/batch_items", url_params)
        resp = request_method(
            url,
            json=params,
            auth=(self._api_token, "")
        )
        if resp.status_code != 204:
            raise ConstructorError(resp.text)
        else:
            return True

    def add_or_update_batch(self, items, autocomplete_section, **kwargs):
        if not self._api_token:
            raise IOError("You must have an API token to use the Add or Update"
                          "Batch method!")
        kwargs["_force"] = 1
        return self.add_batch(items, autocomplete_section, **kwargs)
        
    def remove(self, item_name, autocomplete_section):
        params = {"item_name": item_name,
                  "autocomplete_section": autocomplete_section}
        url = self._make_url("v1/item")
        if not self._api_token:
            raise IOError(
                "You must have an API token to use the Remove method!")
        resp = requests.delete(
            url,
            json=params,
            auth=(self._api_token, "")
        )
        if resp.status_code != 204:
            raise ConstructorError(resp.text)
        else:
            return True

    def remove_batch(self, items, autocomplete_section):
        if not self._api_token:
            raise IOError(
                "You must have an API token to use the Remove Batch method!")
        url_params = {}
        params = {"items": items, "autocomplete_section": autocomplete_section}
        url = self._make_url("v1/batch_items", url_params)
        resp = requests.delete(
            url,
            json=params,
            auth=(self._api_token, "")
        )
        if resp.status_code != 204:
            raise ConstructorError(resp.text)
        else:
            return True

    def modify(self, item_name, autocomplete_section, **kwargs):
        params = {"item_name": item_name,
                  "autocomplete_section": autocomplete_section}
        if "suggested_score" in kwargs:
            params["suggested_score"] = kwargs["suggested_score"]
        if "keywords" in kwargs:
            params["keywords"] = kwargs["keywords"]
        if "url" in kwargs:
            params["url"] = kwargs["url"]
        if "new_item_name" in kwargs:
            params["new_item_name"] = kwargs["new_item_name"]
        if "description" in kwargs:
            params["description"] = kwargs["description"]
        if "image_url" in kwargs:
            params["image_url"] = kwargs["image_url"]
        url = self._make_url("v1/item")
        if not self._api_token:
            raise IOError(
                "You must have an API token to use the Modify method!")
        resp = requests.put(
            url,
            json=params,
            auth=(self._api_token, "")
        )
        if resp.status_code != 204:
            raise ConstructorError(resp.text)
        else:
            return True

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
        resp = requests.post(
            url,
            json=params,
            auth=(self._api_token, "")
        )
        if resp.status_code != 204:
            raise ConstructorError(resp.text)
        else:
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
        resp = requests.post(
            url,
            json=params,
            auth=(self._api_token, "")
        )
        if resp.status_code != 204:
            raise ConstructorError(resp.text)
        else:
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
        resp = requests.post(
            url,
            json=params,
            auth=(self._api_token, "")
        )
        if resp.status_code != 204:
            raise ConstructorError(resp.text)
        else:
            return True
