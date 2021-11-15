'''Custom exceptions'''

class ConstructorException(Exception):
    '''Custom Constructor.io Exception'''

class HttpException(ConstructorException):
    '''Custom HTTP exception'''

    def __init__(self, message, status, status_text, url, headers): # pylint: disable=too-many-arguments
        self.message = message
        self.status = status
        self.status_text = status_text
        self.url = url
        self.headers = headers

        super().__init__(self.message)
