from typing import Optional


class Template:
    def __init__(self, path: str):
        with open(path, 'r') as file:
            self._template = file.read()

    def substitute(self, context: Optional[dict]) -> str:
        if not context:
            return self._template
