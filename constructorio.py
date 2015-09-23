import requests
import urllib
import simplejson

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
############## just this one, and then poke it about
        url = self._makeUrl("v1/add/") and stuff
        resp = requests.get(url, auth=(self._apiToken, ""))
        pass

    def remove(self):
        pass

    def modify(self):
        pass

    def track_conversion(self, term, autocomplete_section):
        pass

    def track_click_through(self, term, autocomplete_section):
        pass

    def track_search(self, term, autocomplete_section):
        pass
