from constructorio_python.modules.autocomplete import Autocomplete
from constructorio_python.modules.search import Search
from constructorio_python.modules.browse import Browse
from constructorio_python.modules.recommendations import Recommendations

class ConstructorIO:
    def __init__(self) -> None:
        self.autocomplete = Autocomplete()
        self.search = Search()
        self.browse = Browse()
        self.recommendations = Recommendations()
