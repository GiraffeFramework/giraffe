from http.server import HTTPServer
from typing import List

from .routes import Route

import re


class GiraffeServer(HTTPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)

        self.routes: List[Route] = []
        self.root: str = ''
