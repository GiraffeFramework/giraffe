from typing import Any, Optional, Tuple


def _is_valid(value: Any, expected_type: Any, name: str) -> bool:
    if value is not None and not isinstance(value, expected_type):
        raise TypeError(f"Invalid value for {name}, expected {expected_type.__name__}")
        
    return True


class Field:
    def __init__(self, name: str, nullable: bool=True, primary_key: bool=False, unique: bool=False):
        self.name: str | None = name if _is_valid(name, str, "name") else None
        self.nullable = nullable
        self.primary_key = primary_key
        self.unique = unique

        if not self.name:
            return ValueError(f"Invalid field, name= argument is required.")


class String(Field):
    def __init__(self, name: str, max_length: Optional[int] = 0, min_length: Optional[int] = 0, default: Optional[str] = None, nullable: bool=True, primary_key: bool=False, unique: bool=False) -> None:
        super().__init__(name, nullable, primary_key, unique)

        if max_length and _is_valid(max_length, int, "max_length"):
            self.max_length = max_length

        if min_length and _is_valid(min_length, int, "min_length"):
            self.min_length = min_length

        if default and _is_valid(default, int, "default"):
            if not self.valid(default):
                raise ValueError(f"Invalid default '{default}' provided")
            
            self.default = default

    def valid(self, value) -> Tuple[bool, str]:
        if self.max_length and len(value) > self.max_length:
            return False, "Maximum length exceeded"
        
        if self.min_length and len(value) < self.min_length:
            return False, "Minimum length not reached"
        
        return True, ""


class Integer(Field):
    def __init__(self, name: str, default: Optional[int], nullable: bool=True) -> None:
        super().__init__(name, nullable)

        if default and _is_valid(default, int, "default"):
            self.default = default


class Float(Field):
    def __init__(self, name: str, default: Optional[float], nullable: bool=True) -> None:
        super().__init__(name, nullable)

        if default and _is_valid(default, int, "default"):
            self.default = default


class Date(Field):
    def __init__(self, name: str, default: Optional[Any], nullable: bool=True) -> None:
        super().__init__(name, nullable)

        if default and _is_valid(default, int, "default"):
            self.default = default

