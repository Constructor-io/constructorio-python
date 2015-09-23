import requests

class ConstructorIO(object):
    VERSION = "1.0.0"

    def __init__(self, api_key, autocomplete_key, url="ac.cnstrc.com"):
        self._api_key = api_key
        self._autocomplete_key = ac_key
        self._url = url

    def __version__(self):
        return VERSION

    def _make_url(self):
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
