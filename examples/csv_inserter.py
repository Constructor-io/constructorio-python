import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
# hack for easy import of the library

import csv
import webbrowser
from constructorio.ConstructorIO import ConstructorIO

if __name__ == "__main__":
    api_token = raw_input("enter api token (enter q to quit) : ")
    if api_token == "q":
        print "toodles!"
        sys.exit(0)
    autocomplete_key = raw_input("enter autocomplete key (enter q to quit) : ")
    if autocomplete_key == "q":
        print "toodles!"
        sys.exit(0)
    autocomplete_section = raw_input("enter autocomplete section (enter q to quit) : ")
    if autocomplete_section == "q":
        print "toodles!"
        sys.exit(0)
    constructor = ConstructorIO(api_token, autocomplete_key) # is that right?
    with open("example.csv") as csv_file:
        example_csv = csv.DictReader(csv_file)
        for row in example_csv:
            print "row: ", row
            print "sending this row over to your Constructor.io account..."
            constructor.add(row["term"],
                            autocomplete_section,
                            score=row["score"])
    print "let's go see the terms you added!"
    webbrowser_resp = raw_input("Go to constructor.io right now? (y/n) (n)")
    if webbrowser_resp == "y":
        print "ok! let's go!"
        webbrowser.open("http://constructor.io/dashboard")
    else:
        print "ok, then just go to constructor.io/dashboard some other time"
