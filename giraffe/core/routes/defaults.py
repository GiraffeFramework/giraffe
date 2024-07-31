from .routes import Routes

from pathlib import Path


default_routes = Routes()


def _response(request, content: str, content_type: str, status: int) -> int:
    request.send_response(status)
    request.send_header('Content-type', content_type)
    request.end_headers()

    return request.wfile.write(content.encode())


@default_routes.get('/static/<type>/<name>')
def get_static_path(request, type, name):
    path = Path(request.server.root) / 'static' / type / name

    if not path.exists():
        return _response(request, "<h1>Not found</h1>", 'text/html', 404)

    with open(path, 'r') as file:
        content = file.read()

    return _response(request, content, f'text/{name.split(".")[1]}', 200)


@default_routes.get('/_cached/<type>/<name>')
def get_cached_path(request, type, name):
    path = Path(request.server.root) / '_cached' / type / name

    if not path.exists():
        return _response(request, "<h1>Not found</h1>", 'text/html', 404)

    with open(path, 'r') as file:
        content = file.read()

    return _response(request, content, f'text/{name.split(".")[1]}', 200)
