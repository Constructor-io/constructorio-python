'''Custom exceptions'''

class ConstructorException(Exception):
    '''Custom Constructor.io Exception'''
    def __init__(self, message):
        super().__init__(message)

