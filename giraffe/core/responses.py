from typing import Union

from http.server import BaseHTTPRequestHandler

import json

def response(request: BaseHTTPRequestHandler, content: str = '', status: int = 200) -> None:
    if not content:
        status = 204

    request.send_response(status)
    request.send_header('Content-type', 'text/plain')
    request.end_headers()

    return request.wfile.write(content.encode())


def json_response(request: BaseHTTPRequestHandler, data: Union[dict, list], status: int = 200) -> None:
    if not isinstance(data, dict) or not isinstance(data, list):
        raise TypeError('data must be a dict or a list')
    
    if not data:
        status = 204

    request.send_response(status)
    request.send_header('Content-type', 'application/json')
    request.end_headers()

    json_data = json.dumps(data)

    return request.wfile.write(json_data.encode())
