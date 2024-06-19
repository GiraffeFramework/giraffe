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
        handler, params = self._match_route('GET')

        if not handler:
            return self.send_error(params['status'], params['error'])

        return handler(self, **params)
    
    def do_POST(self):
        handler, params = self._match_route('POST')

        if not handler:
            return self.send_error(params['status'], params['error'])

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

    def _match_route(self, method: str) -> Tuple[Optional[Callable], Dict[str, Any]]:
        if not self.server.routes:
            return None, {'status' : 404, 'error' : 'Not Found'}
            
        for route in self.server.routes:
            match = route.pattern.match(self.path)

            if not match:
                continue

            if not route.method == method:
                if match:
                    return None, {'status' : 405, 'error' : 'Method Not Allowed'}

                continue

            params = match.groupdict()

            return route.handler, params

        return None, {'status' : 404, 'error' : 'Not Found'}
