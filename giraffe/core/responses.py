from http.server import BaseHTTPRequestHandler

from typing import Union


def response(content: str = '', status: int = 200) -> None:
    if not content:
        status = 204

    # fix this shit

    handler.send_response(status)
    handler.send_header('Content-type', 'text/plain')
    handler.end_headers()

    handler.wfile.write(content.encode())


def json_response(data: Union[dict, list], status: int=200) -> None:
    if not data:
        status = 204

    handler = BaseHTTPRequestHandler()

    handler.send_response(code=status)
    handler.send_header('Content-type', 'application/json')
    handler.end_headers()

    return handler.wfile.write(content.encode())


def render(template: str, status: int) -> None:
    pass