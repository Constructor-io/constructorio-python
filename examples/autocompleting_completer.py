import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
# hack for easy import of the library

from constructorio.ConstructorIO import ConstructorIO

if __name__ == "__main__":
    # Standard English Autocomplete
    constructor = ConstructorIO("---", "P03bVBcmyYjSG1ZQyD4V")
    while True:
        misspelled = raw_input("Type mispelled things and press enter! (q to quit) > ")
        if misspelled == "q":
            break
        else:
            query = constructor.query(misspelled)
            suggested_queries = [s["value"] for s in query["suggestions"]]
            print "suggested queries: ", " | ".join(suggested_queries)
