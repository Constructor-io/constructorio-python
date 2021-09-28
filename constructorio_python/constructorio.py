'''ConstructorIO Python Client'''

__version__ = 1.0

from constructorio_python.modules.autocomplete import Autocomplete
from constructorio_python.modules.browse import Browse
from constructorio_python.modules.recommendations import Recommendations
from constructorio_python.modules.search import Search


class ConstructorIO:
    '''ConstructorIO Python Client'''

    def __init__(self, options) -> None:
        api_key = options.get('api_key')
        api_token = options.get('api_token')
        security_token = options.get('security_token')
        version = options.get('version')
        service_url = options.get('service_url')
        requests = options.get('requests')

        if not api_key or not isinstance(api_key, str):
            raise Exception('API key is a required parameter of type string')

        self.__options = {
            'api_key': api_key,
            'api_token': api_token or '',
            'security_token': security_token or '',
            'version': version or __version__,
            'service_url': service_url or 'https://ac.cnstrc.com',
            'requests': requests,
        }

        self.autocomplete = Autocomplete(self.__options)
        self.search = Search()
        self.browse = Browse()
        self.recommendations = Recommendations()
