from typing import Any, Optional, Tuple


class Field:
    def __init__(self, name: Optional[str] = None, max_length: Optional[int] = None, min_length: Optional[int] = None):
        self.name: str | None = name if self._is_valid(name, str, "name") else None
        self.max_length: int | None = max_length if self._is_valid(max_length, int, "max_length") else 0
        self.min_length: int | None = min_length if self._is_valid(min_length, int, "min_length") else 0

        if not self.name:
            return ValueError(f"Invalid field, name= argument is required.")

    def _is_valid(self, value: Any, expected_type: Any, name: str) -> bool:
        if value is not None and not isinstance(value, expected_type):
            raise TypeError(f"Invalid value for {name}, expected {expected_type.__name__}")
        
        return True
    
    def valid(self, value) -> Tuple[bool, str]:
        if self.max_length and len(value) > self.max_length:
            return False, "Maximum length exceeded"
        
        if self.min_length and len(value) < self.min_length:
            return False, "Minimum length not reached"
        
        return True, ""


class String(Field):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class Integer(Field):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class Float(Field):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class Date(Field):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
