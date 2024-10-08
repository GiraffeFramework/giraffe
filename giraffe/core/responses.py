from typing import Union, Optional

from .html.template import Template
from .requests import RequestHandler

import orjson
import os


def response(request: RequestHandler, content: bytes, content_type: str, status: int = 200) -> int:
    if not content:
        status = 204

    request.send_response(status)
    request.send_header('Content-type', content_type)
    request.end_headers()

    return request.wfile.write(content)


def text_response(request: RequestHandler, content: str = '', status: int = 200) -> int:
    return response(request, content.encode(), 'text/plain', status)
    


def json_response(request: RequestHandler, data: Union[dict, list], status: int = 200) -> int:
    if not isinstance(data, dict) and not isinstance(data, list):
        raise TypeError('data must be a dict or a list')

    return response(request, orjson.dumps(data), 'application/json', status)


def html_response(request: RequestHandler, template: str, status: int = 200, context: Optional[dict]=None) -> int:
    path = os.path.join(request.server.root, 'templates', template)

    if not os.path.exists(path):
        try:
            Template(template, False).substitute(context)
            
        except:
            raise FileNotFoundError(f'Template {template} not found')
    
    else:
        template = Template(path, True, request.server.root).substitute(context)
    
    return response(request, template.encode(), 'text/html', status)
