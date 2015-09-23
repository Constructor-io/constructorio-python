import requests
import urllib
import simplejson
import sys
import logging

class ConstructorIO(object):
    VERSION = "1.0.0"

    def __init__(self, apiToken="", autocompleteKey="", protocol="https", host="ac.cnstrc.com"):
        self._apiToken = apiToken
        self._autocompleteKey = autocompleteKey
        self._protocol = protocol
        self._host = host

    def __version__(self):
        return VERSION

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
        return resp

    def add(self, item_name, autocomplete_section):
        params = {"item_name": item_name, "autocomplete_section": autocomplete_section}
        url = self._makeUrl("v1/item")
        print url
        return requests.post(url, data=params, auth=(self._apiToken, ""))

    def remove(self, item_name, autocomplete_section):
        params = {"item_name": item_name, "autocomplete_section": autocomplete_section}
        url = self._makeUrl("v1/add/", params)
        return requests.get(url, auth=(self._apiToken, ""))

    def modify(self, item_name, autocomplete_section):
        params = {"item_name": item_name, "autocomplete_section": autocomplete_section}
        url = self._makeUrl("v1/add/", params)
        return requests.get(url, auth=(self._apiToken, ""))

    def track_conversion(self, term, autocomplete_section):
        params = {
            "term": term,
            "autocomplete_section": autocomplete_section,
        }
        url = self._makeUrl("v1/conversion")
        resp = requests.post(
            url,
            json=params,
            auth=(self._apiToken, "")
        )
        return resp

    def track_click_through(self, term, autocomplete_section):
        params = {
            "term": term,
            "autocomplete_section": autocomplete_section,
        }
        url = self._makeUrl("v1/click_through")
        resp = requests.post(
            url,
            json=params,
            auth=(self._apiToken, "")
        )
        return resp

    def track_search(self, term, autocomplete_section, num_results=1):
        params = {
            "term": term,
            "autocomplete_section": autocomplete_section,
            "num_results": num_results
        }
        url = self._makeUrl("v1/search")
        resp = requests.post(
            url,
            json=params,
            auth=(self._apiToken, "")
        )
        return resp
