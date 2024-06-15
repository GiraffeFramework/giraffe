from typing import Optional


class Template:
    def __init__(self, template: str, is_file: bool=True):
        if is_file:
            with open(template, 'r') as file:
                self._template = file.read()

        else:
            self._template = template

    def substitute(self, context: Optional[dict]) -> str:
        if not context:
            return self._template
        
        return self._template
