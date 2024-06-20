from typing import Dict
    

class Model:
    def __init__(self, body: Any=None) -> None:
        self._body = body

        return None

    def create(self, *args, **kwargs) -> Tuple['Model', Dict]:
        return None, {}
