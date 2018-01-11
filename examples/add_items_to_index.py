"""
This example shows how to add items to your index.
Items used: /examples/items_for_indexation.csv

More: https://constructor.io/docs/#autocomplete-items
"""

import os
import csv
import webbrowser
from six.moves import input

from constructor_io import ConstructorIO

if __name__ == "__main__":
    api_token = input("Enter api token: ")
    key = input("Enter key: ")
    autocomplete_section = input("Enter autocomplete section: ")

    constructor_instance = ConstructorIO(api_token, key)

    items_file_path = os.path.dirname(os.path.realpath(__file__)) + \
        "/items_for_indexation.csv"

    with open(items_file_path) as csv_file:
        example_csv = csv.DictReader(csv_file)
        for row in example_csv:
            print("Row: " + str(row))
            print("Sending this row over to your Constructor.io account...")
            constructor_instance.add(
                item_name=row["term"],
                autocomplete_section=autocomplete_section,
                score=row["score"]
            )

    print("Let's go see the terms you added!")

    if input("Go to constructor.io right now? (y/n)") == "y":
        print("Ok! let's go!")
        webbrowser.open("http://constructor.io/dashboard")
    else:
        print("Ok, then just go to constructor.io/dashboard some other time")
