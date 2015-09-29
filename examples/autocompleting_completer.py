import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
# hack for easy import of the library

import readline
from constructorio import ConstructorIO

class Completer(object):
    def __init__(self, autocompleteKey):
        self.constructor = ConstructorIO("invalid", autocompleteKey)

    def complete(self, text, state):
        query = self.constructor.query(text)
        if len(query["suggestions"]) == 0:
            state -= 1
        else:
            return query["suggestions"][0]["value"]

if __name__ == "__main__":
    # Standard English Autocomplete
    constructor = ConstructorIO("---", "P03bVBcmyYjSG1ZQyD4V")
    while True:
        misspelled = raw_input("Type mispelled things and press enter! (q to quit) > ")
        if misspelled == "q":
            break
        else:
            print constructor.query(misspelled)
