import requests
import urllib

class ConstructorIO(object):
    def __init__(self, apiToken, autocompleteKey, protocol="http", host="ac.cnstrc.com"):
        """
        If you use HTTPS, you need a different version of requests
        """
        self._apiToken = apiToken
        self._autocompleteKey = autocompleteKey
        self._protocol = protocol
        self._host = host

    def _serializeParams(self, params):
        return urllib.urlencode(params)

    def _makeUrl(self, endpoint, params=None):
        if not params:
            params = {}
        params["autocomplete_key"] = self._autocompleteKey
        return "{0}://{1}/{2}?{3}".format(self._protocol, self._host, endpoint, self._serializeParams(params))

    def query(self, queryStr):
        url = self._makeUrl("autocomplete/" + queryStr)
        resp = requests.get(url)
        if resp.status_code != 200:
            raise IOError(resp.text)
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
        url = self._makeUrl("v1/item")
        resp = requests.post(
            url,
            json=params,
            auth=(self._apiToken, "")
        )
        if resp.status_code != 204:
            raise IOError(resp.text)
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
        url = self._makeUrl("v1/item")
        resp = requests.delete(
            url,
            json=params,
            auth=(self._apiToken, "")
        )
        if resp.status_code != 204:
            raise IOError(resp.text)
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
        url = self._makeUrl("v1/item")
        resp = requests.put(
            url,
            json=params,
            auth=(self._apiToken, "")
        )
        if resp.status_code != 204:
            raise IOError(resp.text)
        else:
            return True

    def track_conversion(self, term, autocomplete_section, **kwargs):
        params = {
            "term": term,
            "autocomplete_section": autocomplete_section,
        }
        if "item" in kwargs:
            params["item"] = kwargs["item"]
        url = self._makeUrl("v1/conversion")
        resp = requests.post(
            url,
            json=params,
            auth=(self._apiToken, "")
        )
        if resp.status_code != 204:
            raise IOError(resp.text)
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
        url = self._makeUrl("v1/click_through")
        resp = requests.post(
            url,
            json=params,
            auth=(self._apiToken, "")
        )
        if resp.status_code != 204:
            raise IOError(resp.text)
        else:
            return True

    def track_search(self, term, autocomplete_section, **kwargs):
        params = {
            "term": term,
            "autocomplete_section": autocomplete_section,
        }
        if "num_results" in kwargs:
            params["num_results"] = kwargs["num_results"]
        url = self._makeUrl("v1/search")
        resp = requests.post(
            url,
            json=params,
            auth=(self._apiToken, "")
        )
        if resp.status_code != 204:
            raise IOError(resp.text)
        else:
            return True
