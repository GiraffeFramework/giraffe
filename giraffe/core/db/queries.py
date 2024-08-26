from typing import TypeVar, Generic, List, Type, Optional, Dict, Any, TYPE_CHECKING, Tuple

from .connections import query_all, query_one, change_db
from .fields import Field


if TYPE_CHECKING:
    from .models import Model


T = TypeVar('T', bound='Model')


class Query(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def create(self, *required_fields: Field) -> Tuple[Optional[T], Dict]:
        body: Optional[Dict] = self.model()._body

        if not body:
            return None, {'status' : 400, 'error' : "No body"}

        invalid_fields: List = []

        for field in required_fields:
            if not field.name in body:
                invalid_fields.append(field.name)

            value = body[field.name]
            valid, error = field.valid(value)

            if not valid:
                invalid_fields.append(f'{field.name} ({error})')

        if invalid_fields:
            return None, {'status' : 400, 'error' : f"Invalid {', '.join(invalid_fields)}"}
        
        fields = ', '.join(body.keys())
        values = ', '.join(f"'{body[field]}'" for field in body.keys())

        result = change_db(f"INSERT INTO {self.model().get_tablename()} ({fields}) VALUES ({values})")

        return self.model(), {}
    
    def latest(self, date_field: str) -> Optional[T]:
        if not self.model()._field_exists(date_field):
            raise ValueError(f"Cannot return by date field {date_field}")

        # Replace with actual query logic
        query = f"SELECT * FROM {self.model().get_tablename()} ORDER BY {date_field} DESC LIMIT 1;"
        
        result = query_one(query)

        if result:
            return self.model()
        
        return None
