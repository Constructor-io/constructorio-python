# Constructor.io Python Client

[![Version](https://img.shields.io/pypi/v/constructor-io.svg)](https://pypi.python.org/pypi/constructor-io)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A Python client for [Constructor.io](http://constructor.io/). [Constructor.io](http://constructor.io/) provides search as a service that optimizes results using artificial intelligence (including natural language processing, re-ranking to optimize for conversions, and user personalization).

## Documentation
Full API documentation is available on [Github Pages](https://constructor-io.github.io/constructorio-python)

## Requirements

Requesting results from your back-end can be useful in order to control result rendering logic on your server, or augment/hydrate results with data from another system. However, a back-end integration has additional requirements compared to a front-end integration. Please review the [Additional Information For Backend Integrations](https://github.com/Constructor-io/constructorio-python/wiki/Additional-Information-for-Backend-Integrations) article within the wiki for more detail.

## 1. Install

```
pip install constructor-io
```

## 2. Retrieve an API key and token

You can find this in your [Constructor.io dashboard](https://constructor.io/dashboard). Contact sales if you'd like to sign up, or support if you believe your company already has an account.

## 3. Implement the Client

Once imported, an instance of the client can be created as follows:

```python
from constructor_io.constructor_io import ConstructorIO

constructorio = ConstructorIO({
    "api_key": "YOUR API KEY",
})
```

## 4. Retrieve Results

After instantiating an instance of the client, four modules will be exposed as properties to help retrieve data from Constructor.io: `search`, `browse`, `autocomplete`, and `recommendations`.

## 5. Track Search Results Loaded

After you render search results from your back-end, send a `search_result_load` event with the `tracker` module. Pass the `result_id` from the search response so the event is tied to that response. `client_id` and `session_id` are required.

```python
user_parameters = {
    "client_id": "7a43138f-c87b-29c0-872d-65b00ed0e392",
    "session_id": 1,
    "user_ip": "127.0.0.1",
    "user_agent": "Mozilla/5.0 ...",
}

search_results = constructorio.search.get_search_results("T-Shirt", {"section": "Products"}, user_parameters)

constructorio.tracker.track_search_results_loaded(
    "T-Shirt",
    {
        "result_id": search_results["result_id"],
        "result_count": search_results["response"]["total_num_results"],
        "items": [{"item_id": result["data"]["id"]} for result in search_results["response"]["results"]],
        "section": "Products",
    },
    user_parameters,
)
```

## Development

```bash
make install                            # install dependencies
pipenv run pylint constructor_io  # run lint
pipenv run pytest .                     # run tests with coverage report
make docs                               # output documentation to `./docs` directory
```


