from .requests import RequestHandler
from .routes import Routes
from .server import GiraffeServer

import sys
import os


class Giraffe:
    def __init__(self, name: str, port: int = 4000):
        self._name = name
        self._port = port
        self._routes = []

    def add_routes(self, routes: Routes):
        self._routes.extend(routes.routes)

    def _valid_port(self, port: int) -> bool:
        return 0 < port < 65536

    def start(self):
        if not self._valid_port(self._port):
            raise ValueError('Invalid port')

        server_address = ('', self._port)
        httpd = GiraffeServer(server_address, RequestHandler)

        httpd.routes = self._routes
        httpd.root = os.path.join(os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__)), 'app') # type: ignore + rewrite

        print(f"Starting server '{self._name}' on http://127.0.0.1:{self._port}")
        
        try:
            print(f"'{self._name}' started")
            httpd.serve_forever()

        except KeyboardInterrupt:

            print(f"Stopping server '{self._name}'")
            httpd.server_close()

        else:
            print(f"Server failed to start")
            httpd.server_close()
