# Constructor-IO Python Client [![Build](https://travis-ci.org/Constructor-io/constructorio-python.svg?branch=master)](https://travis-ci.org/Constructor-io/constructorio-python) [![Version](https://img.shields.io/pypi/v/constructor-io.svg)](https://pypi.python.org/pypi/constructor-io) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)



A Python package for the [Constructor.io API](http://constructor.io/docs).  Constructor.io provides a lightning-fast, typo-tolerant autocomplete service that ranks your users' queries by popularity to let them find what they're looking for as quickly as possible.

## Installation

```
pip install constructor-io
```

## Usage

Here is a simple example how autocomplete works:
```
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
```

Try it:
```
python examples/autocomplete.py
```

![Run example](https://github.com/Constructor-io/constructorio-python/raw/master/run_example.gif)

Check [examples folder](examples). More you can find in our most up-to-date API [documentation](https://constructor.io/docs/?python#).
