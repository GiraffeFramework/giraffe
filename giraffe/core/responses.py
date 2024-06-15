from typing import Union, Optional

from .requests import RequestHandler
from .templates import Template

import json
import os


def response(request: RequestHandler, content: str = '', status: int = 200) -> int:
    if not content:
        status = 204

    request.send_response(status)
    request.send_header('Content-type', 'text/plain')
    request.end_headers()

    return request.wfile.write(content.encode())


def json_response(request: RequestHandler, data: Union[dict, list], status: int = 200) -> int:
    if not isinstance(data, dict) or not isinstance(data, list):
        raise TypeError('data must be a dict or a list')
    
    if not data:
        status = 204

    request.send_response(status)
    request.send_header('Content-type', 'application/json')
    request.end_headers()

    json_data = json.dumps(data)

    return request.wfile.write(json_data.encode())


def html_response(request: RequestHandler, template_name: str, context: Optional[dict]=None, status: int = 200) -> int:
    path = os.path.join(request.server.root, 'templates', template_name)

    if not os.path.exists(path):
        raise FileNotFoundError(f'Template {template_name} not found')

    request.send_response(status)
    request.send_header('Content-type', 'text/html')
    request.end_headers()

    template = Template(path).substitute(context)

    return request.wfile.write(template.encode())
