Constructor-IO Python Client
=====

A Python package for the [Constructor.io API](http://constructor.io/docs).  Constructor.io provides a lightning-fast, typo-tolerant autocomplete service that ranks your users' queries by popularity to let them find what they're looking for as quickly as possible.

Installation
===

With pip:

    pip install constructorio

API
===

All of these are basically one step away from the RESTFUL interface and the implementation is dead simple.

*Everything just returns a response object from the requests library.*

Usage
---

Create a new instance with your API token and autocomplete key:

    from constructorio import ConstructorIO
    constructor = ConstructorIO(
      apiToken="your API token",
      autocompleteKey="your autocomplete key"
    )
    # both of these are available at https://constructor.io/dashboard

Querying
---

To query the autocomplete from your backend:

(If you are making a website, use our Javascript front-end client, it will be much faster for your users. Like, seriously.)

    >>> resp = constructor.query("a")
    >>> resp.json
    {
      "suggestions": [
        {"value": "ambulance"},
        {"value": "aardvark"},
        {"value": "Aachen"}
      ]
    }

Changing the index
---

To add an item to your autocomplete index:
    
    constructor.add(
        item_name = "boinkamoinka",
        autocomplete_section = "Search Suggestions"
    )

To remove an item from your autocomplete index:
    
    constructor.remove(
        item_name = "boinkamoinka",
        autocomplete_section = "Search Suggestions"
    )

To modify an item in your autocomplete index:

    constructor.modify(
        item_name = "boinkamoinka",
        suggested_score = 100,
        autocomplete_section = "Search Suggestions"
    )

Tracking
---

You can also track behavioral data to improve the rankings of your results.  There are three tracking methods for search, click_through, and conversion:

Tracking a search event:

    constructor.track_search(
      term="xyz",
      num_results=302,
      autocomplete_section="products_autocomplete"
    )

Tracking a click-through event:

    constructor.track_click_through(
      term="xyz",
      item="alphabet soup",
      autocomplete_section="products_autocomplete"
    )

Tracking a click-through event:
    
    constructor.track_conversion(
      term="xyz",
      item="alphabet soup",
      autocomplete_section="products_autocomplete"
    )

