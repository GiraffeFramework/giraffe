from http.server import HTTPServer
from typing import Dict, Callable


class GiraffeServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)

        self.get_routes: Dict[str, Callable] = {}
        self.post_routes: Dict[str, Callable] = {}
        self.root: str = ''
