import re

from typing import Callable, Optional, List, Tuple


class Routes:
    def __init__(self, prefix: str = ''):
        self._prefix = prefix
        self.get_routes: List[Tuple[re.Pattern, Callable]] = []
        self.post_routes: List[Tuple[re.Pattern, Callable]] = []

    def _route_exists(self, route: re.Pattern) -> bool:
        routes = self.get_routes

        if self.post_routes:
            routes.extend(self.post_routes)

        for _route in routes:
            if _route[0].pattern == route:
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
            route = self._generate_route(path)

            if 'GET' in methods:
                self.get_routes.append((route, func))

            if 'POST' in methods:
                self.post_routes.append((route, func))

            return func
        return decorator

    def get(self, path: str) -> Callable:
        return self.route(path, ['GET'])

    def post(self, path: str) -> Callable:
        return self.route(path, ['POST'])
