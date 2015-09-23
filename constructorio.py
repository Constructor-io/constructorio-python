import requests

class ConstructorIO(object):
    VERSION = "1.0.0"

    def __init__(self, apiToken="", autocompleteKey="", protocol="http", host="ac.cnstrc.com"):
        self._apiToken = apiToken
        self._autocompleteKey = autocompleteKey
        self._protocol = protocol
        self._host = host

    def __version__(self):
        return VERSION

    def _serializeParams(self, **params):
        pass

    def _makeUrl(self, endpoint):
        pass

    def query(self, query):
        requests.get(self.url, something, something)
        pass

    def add(self, item_name, autocomplete_section):
        pass

    def remove(self):
        pass

    def modify(self):
        pass

    def track_conversion(self):
        pass

    def track_click_through(self):
        pass

    def track_search(self):
        pass
