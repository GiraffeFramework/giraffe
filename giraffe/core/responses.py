from typing import Union, Optional

from .templates.html import Template
from .requests import RequestHandler

import json
import os


def response(request: RequestHandler, content: str, content_type: str, status: int = 200) -> int:
    if not content:
        status = 204

    request.send_response(status)
    request.send_header('Content-type', content_type)
    request.end_headers()

    return request.wfile.write(content.encode())


def text_response(request: RequestHandler, content: str = '', status: int = 200) -> int:
    return response(request, content, 'text/plain', status)
    


def json_response(request: RequestHandler, data: Union[dict, list], status: int = 200) -> int:
    if not isinstance(data, dict) and not isinstance(data, list):
        raise TypeError('data must be a dict or a list')

    return response(request, json.dumps(data), 'application/json', status)


def html_response(request: RequestHandler, template: str, status: int = 200, context: Optional[dict]=None) -> int:
    if template.startswith('templates/'):
        path = os.path.join(request.server.root, 'templates', template)

        if not os.path.exists(path):
            raise FileNotFoundError(f'Template {template} not found')
        
        template = Template(path, True).substitute(context)
    
    else:
        Template(template, False).substitute(context)

    return response(request, template, 'text/html', status)
