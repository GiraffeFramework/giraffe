import re

from typing import Callable, List


class Route:
    def __init__(self, pattern: re.Pattern, method: str, handler: Callable):
        self.pattern: re.Pattern = pattern
        self.method: str = method
        self.handler: Callable = handler


class Routes:
    def __init__(self, prefix: str = ''):
        self._prefix = prefix
        self.routes: List[Route] = []

    def _route_exists(self, compiled_pattern: re.Pattern) -> bool:
        for route in self.routes:
            if route.pattern.pattern == compiled_pattern.pattern:
                return True

        return False

    def _generate_route(self, path: str) -> re.Pattern:
        full_path = self._prefix + (path if path.startswith('/') else '/' + path)
        path_regex = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', full_path)
        compiled_regex = re.compile(f'^{path_regex}$')
        
        if self._route_exists(compiled_regex):
            raise ValueError(f'Route for {full_path} already exists')

        return compiled_regex

    def route(self, path: str, methods: List[str] = ['GET']) -> Callable:
        def decorator(func: Callable) -> Callable:
            for method in methods:
                compiled_pattern = self._generate_route(path)
                self.routes.append(Route(compiled_pattern, method, func))

            return func
        
        return decorator

    def get(self, path: str) -> Callable:
        return self.route(path, ['GET'])

    def post(self, path: str) -> Callable:
        return self.route(path, ['POST'])
