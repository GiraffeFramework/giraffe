from http.server import HTTPServer

from .requests import RequestHandler
from .routes import Routes


class Giraffe:
    def __init__(self, name: str, port: int = 4000):
        self.name = name
        self.port = port
        self.get_routes = {}
        self.post_routes = {}

    def add_routes(self, routes: Routes):
        self.get_routes.update(routes.get_routes)
        self.post_routes.update(routes.post_routes)

    def _valid_port(self, port: int) -> bool:
        return 0 < port < 65536

    def start(self):
        if not self._valid_port(self.port):
            raise ValueError('Invalid port')

        server_address = ('', self.port)
        httpd = HTTPServer(server_address, RequestHandler)
        httpd.get_routes = self.get_routes
        httpd.post_routes = self.post_routes

        print(f'Starting server {self.name} on http://127.0.0.1:{self.port}')
        
        try:
            httpd.serve_forever()

        except KeyboardInterrupt:
            print(f'Stopping server {self.name}...')
            httpd.server_close()
