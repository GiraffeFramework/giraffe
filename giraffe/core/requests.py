from http.server import BaseHTTPRequestHandler

from typing import Any, Callable, Dict, Optional, Tuple

from .server import GiraffeServer

import json
import re


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server: GiraffeServer
        self.body: Any
        
    def do_GET(self):
        handler, params = self._match_route(self.server.get_routes)

        if not handler:
            return self.send_error(404, 'Not found')

        return handler(self, **params)
    
    def do_POST(self):
        handler, params = self._match_route(self.server.post_routes)

        if not handler:
            return self.send_error(404, 'Not found')

        content_length = int(self.headers.get('Content-Length', -1))
        content_type = self.headers.get('Content-Type')

        if content_type == 'application/json':
            body = self.rfile.read(content_length)
            
            self.body = json.loads(body)

        elif content_type == 'application/x-www-form-urlencoded':
            body = self.rfile.read(content_length)

            self.body = dict(
                re.findall(r'(\w+)=(.+)', body.decode())
            )

        else:
            return self.send_error(415, 'Unsupported Media Type')

        return handler(self, **params)

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
