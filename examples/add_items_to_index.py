"""
This example shows how to add your items in autocomplete index
Items used: /examples/items_for_indexation.csv

More: https://constructor.io/docs/#autocomplete-items
"""

import csv
import webbrowser

from constructor_io import ConstructorIO

if __name__ == "__main__":
    api_token = raw_input("Enter api token: ")
    autocomplete_key = raw_input("Enter autocomplete key: ")
    autocomplete_section = raw_input("Enter autocomplete section: ")

    constructor_instance = ConstructorIO(api_token, autocomplete_key)

    with open("example.csv") as csv_file:
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

    if raw_input("Go to constructor.io right now? (y/n) (n)") == "y":
        print("Ok! let's go!")
        webbrowser.open("http://constructor.io/dashboard")
    else:
        print("Ok, then just go to constructor.io/dashboard some other time")
