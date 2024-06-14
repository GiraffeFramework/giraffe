class Routes:
    def __init__(self, prefix: str = ''):
        self._prefix = prefix
        self.get_routes = {}
        self.post_routes = {}

    def route(self, path: str, methods: list = ['GET']):
        def decorator(func):
            if not path.startswith('/'):
                full_path = '/' + path

            else:
                full_path = path

            full_path = self._prefix + full_path

            if 'GET' in methods:
                self.get_routes[full_path] = func
            
            if 'POST' in methods:
                self.post_routes[full_path] = func

            return func
        
        return decorator
