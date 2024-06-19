from typing import Union, Optional

from .requests import RequestHandler
from .html import Template

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
    if not isinstance(data, dict) and not isinstance(data, list):
        raise TypeError('data must be a dict or a list')
    
    if not data:
        status = 204

    request.send_response(status)
    request.send_header('Content-type', 'application/json')
    request.end_headers()

    json_data = json.dumps(data)

    return request.wfile.write(json_data.encode())


def html_response(request: RequestHandler, template: str, status: int = 200, context: Optional[dict]=None) -> int:
    if template.startswith('<%loaded%>'):
        template = template[10:]

        Template(template, False).substitute(context)
    
    else:
        path = os.path.join(request.server.root, 'templates', template)

        if not os.path.exists(path):
            raise FileNotFoundError(f'Template {template} not found')
        
        template = Template(path, True).substitute(context)

    request.send_response(status)
    request.send_header('Content-type', 'text/html')
    request.end_headers()

    return request.wfile.write(template.encode())
