import sys
import os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
# hack for easy import of the library

import readline
from constructorio import ConstructorIO

COMMANDS = ['extra', 'extension', 'stuff', 'errors',
                    'email', 'foobar', 'foo']

def complete(text, state):
    for cmd in COMMANDS:
        if cmd.startswith(text):
            if not state:
                return cmd
            else:
                state -= 1

if __name__ == "__main__":
    readline.parse_and_bind("tab: complete")
    readline.set_completer(complete)
    while True:
        var = raw_input("Type mispelled things and press tab! (q to quit) > ")
        if var == "q":
            break
