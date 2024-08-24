from .fields import Field

from typing import Tuple, Dict, Optional, Any, List

from .connections import change_db, query_all, query_one
    

def _schema_from_table_info(table_info: Tuple) -> dict:
    return {
        "name": table_info[1],
        "type": table_info[2],
        "notnull": bool(table_info[3]),
        "dflt_value": table_info[4],
        "pk": bool(table_info[5])
    }


class Model:
    def __init__(self, body: Optional[Dict] = None) -> None:
        self.__tablename__: str = ''
        self._body: Dict | None = body
        self._name: str = self._get_name()

        return None
    
    def _field_exists(self, field: str) -> bool:
        return hasattr(self, field)
    
    def _get_name(self) -> str:
        if self._field_exists('__tablename__') and self.__tablename__:
            return self._valid_table_name(self.__tablename__)
        
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
    def get_schema_changes(cls) -> dict:
        """
        Loop over existing schemas from the databse and compare them to the current schema.

        PRAGMA table_info(table_name) returns a list of tuples with the following structure:  
        [(cid, name, type, notnull, dflt_value, pk), (...)]
        """

        old_schemas: list[tuple] = query_all(f"PRAGMA table_info({cls()._name})")
        schemas: list[dict] = []

        print('old_schemas: ', old_schemas)

        if not old_schemas:
            return cls.get_schema()
        
        for old_schema in old_schemas:
            field: Optional[Field] = cls.__dict__.get(old_schema[1], None)

            if not field:
                schema = _schema_from_table_info(old_schema)
                schema['mode'] = 'delete'

            else:
                schema = field.get_schema(old_schema[1])
                schema['mode'] = 'update'

            schemas.append(schema)

        print('schemas: ', schemas)

        return {"name" : cls()._name, "fields" : schemas, "table" : "alter"}
    
    @classmethod
    def get_schema(cls) -> dict:
        primary_key: bool = False
        schemas: list = []

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

        return {"name" : cls()._name, "fields" : schemas, "table" : "create"}

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

        return query_one(f"SELECT {value if value else '*'} FROM {self._name} ORDER BY {order} DESC")
