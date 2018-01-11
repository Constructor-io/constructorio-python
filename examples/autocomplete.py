"""
The most simple example of autocomplete usage. Try running it!
"""
from six.moves import input

from constructor_io import ConstructorIO

# Listed token and key will work for a small demo :)
API_TOKEN = None
KEY = "P03bVBcmyYjSG1ZQyD4V"

constructor_instance = ConstructorIO(API_TOKEN, KEY)

if __name__ == "__main__":
    while True:
        misspelled = input("Type misspelled things and press enter! > ")
        query = constructor_instance.query(misspelled)
        suggestions = query["suggestions"]
        suggested_queries = [suggestion["value"] for suggestion in suggestions]
        print("Suggested queries: " + " | ".join(suggested_queries))
