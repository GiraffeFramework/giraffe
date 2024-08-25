from typing import TypeVar, Generic, List, Type, Optional, Dict, Any, TYPE_CHECKING

from .connections import query_all, query_one


if TYPE_CHECKING:
    from .models import Model


T = TypeVar('T', bound='Model')

class Query(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
    
    def latest(self, date_field: str) -> Optional[T]:
        if not self.model()._field_exists(date_field):
            raise ValueError(f"Cannot return by date field {date_field}")

        # Replace with actual query logic
        query = f"SELECT * FROM {self.model.name} ORDER BY {date_field} DESC LIMIT 1;"
        result = query_one(query)
        if result:
            return self.model(body=result)
        
        return None
