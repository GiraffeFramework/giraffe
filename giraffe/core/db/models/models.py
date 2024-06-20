from ..fields import Field

from typing import Tuple, Dict, Optional, Any, List
    

class Model:
    def __init__(self, body: Optional[Dict]=None) -> None:
        self._body: Dict | None = body

        return None

    def create(self, *args) -> Tuple[Any, Dict]:
        if not self._body:
            return None, {'status' : 400, 'error' : "No body"}

        invalid_fields: List = []

        for arg in args:
            field: Field = arg

            if not field.name in self._body:
                invalid_fields.append(field.name)

            value = self._body[field.name]
            valid, error = field.valid(value)

            if not valid:
                invalid_fields.append(f'{field.name} ({error})')

        if invalid_fields:
            return None, {'status' : 400, 'error' : f"Invalid {', '.join(invalid_fields)}"}
        
        return None, {'status' : 200, 'error' : "THERE WAS NONE!"}
