from typing import Any

        
class Field:
    def __init__(self, *args, **kwargs) -> None:
        if max_length and self._is_valid(min_length, int, "max_length"):
            self._max_length = max_length

        if min_length and self._is_valid(min_length, int, "min_length"):
            self._min_length = min_length

    def _is_valid(self, value: Any, type: Any, name: str):
        if not isinstance(value, type):
            return TypeError(f"Invalid value for {name}")


class String(Field):
    def __init__(self, *args, **kwargs) -> None:
        return None


class Integer(Field):
    def __init__(self) -> None:
        return None


class Float(Field):
    def __init__(self) -> None:
        return None


class Date(Field):
    def __init__(self) -> None:
        return None