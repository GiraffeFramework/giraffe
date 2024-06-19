from http.server import BaseHTTPRequestHandler

from typing import Any, Callable, Dict, Optional, Tuple

from .server import GiraffeServer

import json
import re


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server: GiraffeServer
        self.body: Any = None

    def do_GET(self):
        self._handle_request('GET')

    def do_POST(self):
        self._handle_request('POST')

    def do_PATCH(self):
        self._handle_request('PATCH')

    def do_PUT(self):
        self._handle_request('PUT')

    def do_DELETE(self):
        self._handle_request('DELETE')

    def _handle_request(self, method: str):
        handler, params = self._match_route(method)

        if not handler:
            return self.send_error(params['status'], params['error'])

        if method in ['POST', 'PUT', 'PATCH']:
            self._parse_body()

        return handler(self, **params)

    def _parse_body(self):
        content_length = int(self.headers.get('Content-Length', -1))
        content_type = self.headers.get('Content-Type')

        if content_length < 0:
            self.send_error(411, 'Length Required')
            return

        body = self.rfile.read(content_length)

        if content_type == 'application/json':
            try:
                self.body = json.loads(body)

            except json.JSONDecodeError:
                self.send_error(400, 'Invalid JSON')

        elif content_type == 'application/x-www-form-urlencoded':
            self.body = dict(re.findall(r'(\w+)=(.+)', body.decode()))

        else:
            self.send_error(415, 'Unsupported Media Type')

    def _match_route(self, method: str) -> Tuple[Optional[Callable], Dict[str, Any]]:
        if not self.server.routes:
            return None, {'status': 404, 'error': 'Not Found'}

        for route in self.server.routes:
            match = route.pattern.match(self.path)

            if not match:
                continue

            if route.method != method:
                if match:
                    return None, {'status': 405, 'error': 'Method Not Allowed'}
                continue

            return route.handler, match.groupdict()

        return None, {'status': 404, 'error': 'Not Found'}
