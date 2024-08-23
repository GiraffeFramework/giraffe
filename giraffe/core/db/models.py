from .fields import Field

from typing import Tuple, Dict, Optional, Any, List

from .connections import change_db, query_all
    

class Model:
    def __init__(self, body: Optional[Dict] = None) -> None:
        self._body: Dict | None = body
        self._name: str = self._get_name()

        return None
    
    def _field_exists(self, field: str) -> bool:
        return hasattr(self, field)
    
    def _get_name(self) -> str:
        if self._field_exists('__tablename__'):
            return self._valid_table_name(self.__tablename__) # type: ignore
        
        return self._valid_table_name(self.__class__.__name__.lower())
    
    def _valid_table_name(self, name: str) -> str:
        if len(name) > 128:
            raise ValueError("Table name cannot be longer than 128 characters")
        
        if not name.isalnum():
            raise ValueError("Table name cannot contain non-alphanumeric characters")
        
        return name
    
    @property
    def name(self) -> str:
        return self._name
    
    @classmethod
    def get_schema(cls) -> dict:
        schemas: list = []
        primary_key: bool = False

        for key, value in cls.__dict__.items():
            if not isinstance(value, Field):
                continue

            if value.primary_key:
                if primary_key:
                    raise ValueError("Model can only have one primary key")
                    
                primary_key = True

            schema = value.get_schema(key)

            schemas.append(schema)

        if not primary_key:
            raise ValueError("Model must have a primary key")

        return {"name" : cls()._name, "fields" : schemas, "table" : "alter"}
    
    def _get_db_schema(self) -> dict:
        query_all(f"PRAGMA table_info({self._name})")

        #query:  PRAGMA table_info(migrations)
        #[(0, 'id', 'INT', 0, None, 1), (1, 'name', 'VARCHAR(10)', 0, None, 0), (2, 'applied_at', 'DATE', 0, None, 0)]

        return {}

    def create(self, *required_fields) -> Tuple[Any, Dict]:
        if not self._body:
            return None, {'status' : 400, 'error' : "No body"}

        invalid_fields: List = []

        for arg in required_fields:
            field: Field = arg

            if not field.name in self._body:
                invalid_fields.append(field.name)

            value = self._body[field.name]
            valid, error = field.valid(value)

            if not valid:
                invalid_fields.append(f'{field.name} ({error})')

        if invalid_fields:
            return None, {'status' : 400, 'error' : f"Invalid {', '.join(invalid_fields)}"}
        
        fields = ', '.join(self._body.keys())
        values = ', '.join(f"'{self._body[field]}'" for field in self._body.keys())

        query = f"INSERT INTO {self._name} ({fields}) VALUES ({values})"

        change_db(query)
        
        return None, {'status' : 200, 'error' : "THERE WAS NONE!"}

    def all(self, order: Optional[str]=None, value: Optional[str]=None) -> List:
        if order and not self._field_exists(order.replace('-', '')):
            raise ValueError(f"Cannot order by {order}")
        
        if value and not self._field_exists(value):
            raise ValueError(f"Cannot return by value {value}")

        return query_all(f"SELECT {value if value else '*'} FROM {self._name}{f' ORDER BY {order}' if order else ''}")
    
    def latest(self, order: str, value: Optional[str]=None) -> List:
        if not self._field_exists(order):
            raise ValueError(f"Cannot return by value {order}")

        return query_all(f"SELECT {value if value else '*'} FROM {self._name} ORDER BY {order} DESC LIMIT 1")
