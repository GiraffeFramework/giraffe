from http.server import HTTPServer
from typing import Dict, Callable

import re


class GiraffeServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)

        self.get_routes: Dict[re.Pattern, Callable] = {}
        self.post_routes: Dict[re.Pattern, Callable] = {}
        self.root: str = ''
