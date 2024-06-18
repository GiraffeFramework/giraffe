import re

from typing import Callable, Optional, List, Tuple

class Routes:
    def __init__(self, prefix: str = ''):
        self._prefix = prefix
        self.get_routes: List[Tuple[re.Pattern, Callable]] = []
        self.post_routes: List[Tuple[re.Pattern, Callable]] = []

    def _route_exists(self, route: Tuple[re.Pattern, Callable], method: Optional[str]) -> bool:
        if method == 'GET':
            for get_route in self.get_routes:
                if get_route[0].pattern == route[0].pattern:
                    return True

            return False

        if method  == 'POST':
            for post_route in self.post_routes:
                if post_route[0].pattern == route[0].pattern:
                    return True

            return False
        
        routes = self.get_routes

        if self.post_routes:
            routes.extend(self.post_routes)

        for _route in routes:
            if _route[0].pattern == route[0].pattern:
                return True
        
        return False

    def route(self, path: str, methods: List[str] = ['GET']) -> Callable:
        def decorator(func: Callable) -> Callable:
            full_path = self._prefix + (path if path.startswith('/') else '/' + path)

            path_regex = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', full_path)
            compiled_regex = re.compile(f'^{path_regex}$')

            route = (compiled_regex, func)

            if 'GET' in methods:
                if self._route_exists(route, 'GET'):
                    raise ValueError('Route already exists')

                self.get_routes.append(route)

            if 'POST' in methods:
                if self._route_exists(route, 'POST'):
                    raise ValueError('Route already exists')

                self.post_routes.append(route)

            return func

        return decorator


    def get(self, path: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            full_path = self._prefix + (path if path.startswith('/') else '/' + path)

            path_regex = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', full_path)
            compiled_regex = re.compile(f'^{path_regex}$')

            route = (compiled_regex, func)

            if self._route_exists(route, 'GET'):
                raise ValueError('Route already exists')

            self.get_routes.append(route)

            return func
        
        return decorator

    def post(self, path: str) -> Callable:
        def decorator(func: Callable) -> Callable:
            full_path = self._prefix + (path if path.startswith('/') else '/' + path)

            path_regex = re.sub(r'<(\w+)>', r'(?P<\1>[^/]+)', full_path)
            compiled_regex = re.compile(f'^{path_regex}$')

            route = (compiled_regex, func)

            if self._route_exists(route, 'POST'):
                raise ValueError('Route already exists')

            self.post_routes.append(route)

            return func
        
        return decorator
