from .requests import RequestHandler
from .routes import Routes
from .server import GiraffeServer

from typing import List

import sys
import os


class Giraffe:
    def __init__(self, name: str, port: int = 4000):
        self._name: str = name
        self._port: int = port
        self._routes: List = []

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
        httpd.root = os.path.join(os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))) # type: ignore + TODO

        print(f"Starting server '{self._name}' on http://127.0.0.1:{self._port}")
        
        try:
            print(f"'{self._name}' started")
            httpd.serve_forever()

        except Exception as e:
            if not isinstance(e, KeyboardInterrupt):
                print(f"Server failed to start: {str(e)}")
            
            httpd.server_close()

        finally:
            print(f"Stopping server '{self._name}'")
            sys.exit(0)
