from http.server import BaseHTTPRequestHandler

from typing import Any, Callable, Dict, Optional, Tuple

from .server import GiraffeServer

import re


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server: GiraffeServer
        
    def do_GET(self):
        handler, params = self._match_route(self.server.get_routes)

        if handler:
            return handler(self, **params)

        self.send_error(404, 'Not Found')

    def do_POST(self):
        self.send_error(400, 'Coming soon')


    def _match_route(self, routes: dict[re.Pattern, Callable]) -> Tuple[Optional[Callable], Dict[str, Any]]:
        if not routes:
            return None, {}
            
        for regex, func in routes.items():
            match = regex.match(self.path)

            if not match:
                continue

            params = match.groupdict()

            return func, params

        return None, {}
