from http.server import BaseHTTPRequestHandler


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in self.server.get_routes: # type: ignore
            return self.server.get_routes[self.path](self) # type: ignore

        self.send_error(404, 'Not Found')

    def do_POST(self):
        self.send_error(400, 'Coming soon')
