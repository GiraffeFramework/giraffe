from http.server import BaseHTTPRequestHandler

from .server import GiraffeServer


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.server: GiraffeServer

    def do_GET(self):
        if self.path in self.server.get_routes:
            return self.server.get_routes[self.path](self)

        self.send_error(404, 'Not Found')

    def do_POST(self):
        self.send_error(400, 'Coming soon')
