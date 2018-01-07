"""
The most simple example of autocomplete usage
"""

from constructor_io import ConstructorIO

# Listed token and key will work for a small demo :)
API_TOKEN = None
AUTOCOMPLETE_KEY = "P03bVBcmyYjSG1ZQyD4V"

constructor_instance = ConstructorIO(API_TOKEN, AUTOCOMPLETE_KEY)

if __name__ == "__main__":
    while True:
        misspelled = raw_input("Type mispelled things and press enter! > ")
        query = constructor_instance.query(misspelled)
        suggestions = query["suggestions"]
        suggested_queries = [suggestion["value"] for suggestion in suggestions]
        print("Suggested queries: " + " | ".join(suggested_queries))
