'''ConstructorIO Python Package'''

from constructor_io import __version__
from constructor_io.helpers.exception import ConstructorException
from constructor_io.modules.autocomplete import Autocomplete
from constructor_io.modules.browse import Browse
from constructor_io.modules.catalog import Catalog
from constructor_io.modules.quizzes import Quizzes
from constructor_io.modules.recommendations import Recommendations
from constructor_io.modules.search import Search
from constructor_io.modules.tasks import Tasks


class ConstructorIO:
    # pylint: disable=too-few-public-methods
    # pylint: disable=too-many-instance-attributes
    '''
        ConstructorIO Python Client

        :param str api_key: Constructor.io API key
        :param str api_token: Constructor.io API token
        :param str security_token: Constructor security token
        :param str service_url: API URL endpoint

        :return: class
    '''

    def __init__(self, options) -> None:
        api_key = options.get('api_key')
        api_token = options.get('api_token', '')
        security_token = options.get('security_token', '')
        version = options.get('version')
        service_url = options.get('service_url')
        requests = options.get('requests')

        if not api_key or not isinstance(api_key, str):
            raise ConstructorException('API key is a required parameter of type string')

        self.__options = {
            'api_key': api_key,
            'api_token': api_token,
            'security_token': security_token,
            'version': version or __version__,
            'service_url': service_url or 'https://ac.cnstrc.com',
            'requests': requests,
        }

        self.autocomplete = Autocomplete(self.__options)
        self.search = Search(self.__options)
        self.browse = Browse(self.__options)
        self.recommendations = Recommendations(self.__options)
        self.catalog = Catalog(self.__options)
        self.tasks = Tasks(self.__options)
        self.quizzes = Quizzes(self.__options)

    def get_options(self):
        '''Get client options'''

        return self.__options

    def set_options(self, options):
        '''Set client options'''

        self.__options = options
