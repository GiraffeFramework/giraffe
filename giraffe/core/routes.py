import re

from typing import Callable, Dict, List

class Routes:
    def __init__(self, prefix: str = ''):
        self._prefix = prefix
        self.get_routes = []
        self.post_routes = []

    def route(self, path: str, methods: List[str] = ['GET']):
        def decorator(func: Callable):
            full_path = self._prefix + (path if path.startswith('/') else '/' + path)

            path_regex = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', full_path)
            compiled_regex = re.compile(f'^{path_regex}$')

            route = (compiled_regex, func)

            if 'GET' in methods:
                self.get_routes.append(route)

            if 'POST' in methods:
                self.post_routes.append(route)

            return func

        return decorator
    