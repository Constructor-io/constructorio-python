import requests
import urllib

class ConstructorError(Exception):
    pass

class ConstructorIO(object):
    def __init__(self, api_token, autocomplete_key, protocol="https", host="ac.cnstrc.com"):
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
        return "{0}://{1}/{2}?{3}".format(self._protocol, self._host, endpoint, self._serialize_params(params))

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

    def add(self, item_name, autocomplete_section, **kwargs):
        params = {"item_name": item_name, "autocomplete_section": autocomplete_section}
        if "suggested_score" in kwargs:
            params["suggested_score"] = kwargs["suggested_score"]
        if "keywords" in kwargs:
            params["keywords"] = kwargs["keywords"]
        if "description" in kwargs:
            params["description"] = kwargs["description"]
        if "url" in kwargs:
            params["url"] = kwargs["url"]
        if "image_url" in kwargs:
            params["image_url"] = kwargs["image_url"]
        url = self._make_url("v1/item")
        if not self._api_token:
            raise IOError("You must have an API token to use the Add method!")
        resp = requests.post(
            url,
            json=params,
            auth=(self._api_token, "")
        )
        if resp.status_code != 204:
            raise ConstructorError(resp.text)
        else:
            return True

    def remove(self, item_name, autocomplete_section, **kwargs):
        params = {"item_name": item_name, "autocomplete_section": autocomplete_section}
        if "suggested_score" in kwargs:
            params["suggested_score"] = kwargs["suggested_score"]
        if "keywords" in kwargs:
            params["keywords"] = kwargs["keywords"]
        if "url" in kwargs:
            params["url"] = kwargs["url"]
        url = self._make_url("v1/item")
        if not self._api_token:
            raise IOError("You must have an API token to use the Remove method!")
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
        params = {"item_name": item_name, "autocomplete_section": autocomplete_section}
        if "suggested_score" in kwargs:
            params["suggested_score"] = kwargs["suggested_score"]
        if "keywords" in kwargs:
            params["keywords"] = kwargs["keywords"]
        if "url" in kwargs:
            params["url"] = kwargs["url"]
        if "new_item_name" in kwargs:
            params["new_item_name"] = kwargs["new_item_name"]
        url = self._make_url("v1/item")
        if not self._api_token:
            raise IOError("You must have an API token to use the Modify method!")
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
            raise IOError("You must have an API token to track click throughs!")
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
