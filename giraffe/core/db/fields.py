from typing import Any, Optional, Tuple, Type


def _is_valid(value: Any, expected_type: Type, name: str) -> bool:
    if value is not None and not isinstance(value, expected_type):
        raise TypeError(f"Invalid value for {name}, expected {expected_type.__name__}")
    
    return True


class Field:
    def __init__(self, type: str, name: str, nullable: bool = True, primary_key: bool = False, unique: bool = False):
        if not _is_valid(name, str, "name"):
            raise ValueError(f"Invalid field, name= argument is required.")
        
        self.value: Any = None
        self.type = type
        self.name = name
        self.nullable = nullable
        self.primary_key = primary_key
        self.unique = unique
        self.default = None
        self.max_length = None
        self.min_length = None

    def valid(self, value: str) -> Tuple[bool, str]:
        if self.max_length and len(value) > self.max_length:
            return False, "Maximum length exceeded"
            
        if self.min_length and len(value) < self.min_length:
            return False, "Minimum length not reached"
            
        return True, ""
    
    def get_schema(self, name: str) -> dict:
        return {
            "name" : name,
            "type": self.type,
            "notnull": not self.nullable,
            "dflt_value": self.default,
            "pk": self.primary_key,
            "mode": "create"
        }


class String(Field):
    def __init__(self, name: str, max_length: Optional[int] = 1, min_length: Optional[int] = 0, default: Optional[str] = None, nullable: bool = True, primary_key: bool = False, unique: bool = False) -> None:
        super().__init__('VARCHAR', name, nullable, primary_key, unique)

        if max_length is not None and _is_valid(max_length, int, "max_length"):
            self.max_length = max_length
            self.type = f"VARCHAR({max_length})"

        if min_length is not None and _is_valid(min_length, int, "min_length"):
            self.min_length = min_length
        
        if default is not None and _is_valid(default, str, "default"):
            if not self.valid(default)[0]:
                raise ValueError(f"Invalid default '{default}' provided")
            
            self.default = default

    def __get__(self, instance: Any, owner: Any) -> str:
        # When the field is accessed, return its value as a string
        return self.value

    def __set__(self, instance: Any, value: str) -> None:
        # When a value is assigned, store it internally
        if not isinstance(value, str):
            raise TypeError("Expected a string")
        self.value = value


class Integer(Field):
    def __init__(self, name: str, default: Optional[int] = None, nullable: bool = True, primary_key: bool = False, unique: bool = False) -> None:
        super().__init__('INT', name, nullable, primary_key, unique)

        if default is not None and _is_valid(default, int, "default"):
            self.default = default


class Float(Field):
    def __init__(self, name: str, default: Optional[float] = None, nullable: bool = True, primary_key: bool = False, unique: bool = False) -> None:
        super().__init__('FLOAT', name, nullable, primary_key, unique)

        if default is not None and _is_valid(default, float, "default"):
            self.default = default


class Date(Field):
    def __init__(self, name: str, nullable: bool = True, primary_key: bool = False, unique: bool = False) -> None:
        super().__init__('DATE', name, nullable, primary_key, unique)


class Fields:
    String = String
    Integer = Integer
    Float = Float
    Date = Date

fields = Fields()
