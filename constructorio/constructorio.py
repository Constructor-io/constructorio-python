import requests

class Constructor:
    VERSION = "1.0.0"

    def __init__(self, api_key, autocomplete_key, url="ac.cnstrc.com"):
        self.api_key = api_key
        self.ac_key = ac_key
        self.url = url

    def __version__(self):
        return VERSION

    def autocomplete(self, query):
        requests.post(self.url, something, something)
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
