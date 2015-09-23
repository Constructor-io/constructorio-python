Contructor-IO Python Client
=====

A Python package for the [Constructor.io API](http://constructor.io/docs).  Constructor.io provides a lightning-fast, typo-tolerant autocomplete service that ranks your users' queries by popularity to let them find what they're looking for as quickly as possible.

API
===

query
---

add
---

remove
---

You can also track behavioral data to improve the rankings of your results.  There are three track_* methods for search, click_through, and conversion:

search
---

    constructor.track_search(
      term="xyz",
      num_results=302,
      autocomplete_section="products_autocomplete"
    )

click_through
---

    constructor.track_click_through(
      term="xyz"
      item="alphabet soup"
      autocomplete_section="products_autocomplete"
    )

conversion
---
    
    constructor.track_conversion(
      term="xyz"
      item="alphabet soup"
      autocomplete_section="products_autocomplete"
    )

