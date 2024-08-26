from .connections import query_all
from .queries import Query
from .fields import Field

from typing_extensions import Self

from typing import Tuple, Dict, Optional, TypeVar, Type
    

def _schema_from_table_info(table_info: Tuple) -> dict:
    return {
        "name": table_info[1],
        "type": table_info[2],
        "notnull": bool(table_info[3]),
        "dflt_value": table_info[4],
        "pk": bool(table_info[5])
    }


T = TypeVar('T', bound='Model')


class Model:
    query: Query[Self]

    def __init__(self, body: Optional[Dict] = None) -> None:
        self._body: Optional[Dict] = body
        self.__tablename__: str = ''

    def __init_subclass__(cls: Type[T], **kwargs):
        super().__init_subclass__(**kwargs)
        cls.query = Query(cls)
    
    def _valid_tablename(self, name: str) -> str:
        if len(name) > 128:
            raise ValueError("Table name cannot be longer than 128 characters")
        
        if not name.replace('_', '').isalnum():
            raise ValueError("Table name cannot contain non-alphanumeric characters")
        
        return name
    
    def field_exists(self, field: str) -> bool:
        return hasattr(self, field)
    
    def get_tablename(self) -> str:
        if self.field_exists('__tablename__') and self.__tablename__:
            return self._valid_tablename(self.__tablename__)
        
        return self._valid_tablename(self.__class__.__name__.lower())
    
    @classmethod
    def get_schema_changes(cls) -> dict:
        """
        Loop over existing schemas from the databse and compare them to the current schema.

        PRAGMA table_info(table_name) returns a list of tuples with the following structure:  
        [(cid, name, type, notnull, dflt_value, pk), (...)]
        """

        old_schemas: list[tuple] = query_all(f"PRAGMA table_info({cls().get_tablename()})")
        schema_keys: list[str] = []
        schemas: list[dict] = []

        print('old_schemas: ', old_schemas)

        if not old_schemas:
            return cls.get_schema()
        
        for old_schema in old_schemas:
            field: Optional[Field] = cls.__dict__.get(old_schema[1], None)

            if field:
                schema = field.get_schema(old_schema[1])
                schema['mode'] = 'update'

            else:
                schema = _schema_from_table_info(old_schema)
                schema['mode'] = 'delete'
                
            schema_keys.append(old_schema[1])
            schemas.append(schema)

        for key, value in cls.__dict__.items():
            if not isinstance(value, Field):
                continue

            if not key in schema_keys:
                schema = value.get_schema(key)
                schema['mode'] = 'create'

        print('schemas: ', schemas)

        return {"name" : cls().get_tablename(), "fields" : schemas, "table" : "alter"}
    
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

            schemas.append(value.get_schema(key))

        if not primary_key:
            raise ValueError("Model must have a primary key")

        return {"name": cls().get_tablename(), "fields": schemas, "table": "create"}
