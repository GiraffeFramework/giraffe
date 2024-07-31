from typing import Callable

from pathlib import Path

from lxml.etree import _Element

import random
import string
import re


class AttributeFunctions:
    def __init__(self, root: str):
        self._root: str = root
        self.functions: dict[str, Callable] = {'grf-minify' : self._minify}

        self._register_functions()

    def _get_name(self, file_type) -> str:
        path = Path(self._root) / '_cached' / file_type

        name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        while (path / f'{name}.{file_type}').exists():
            name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        return name

    def _minify(self, elm: _Element) -> _Element:
        """
        Removes comments, whitespaces, redundant semicolons and newlines.
        """

        path = Path(self._root) / elm.get('href', '')[1:]

        if not path.exists():
            path = Path(self._root) / elm.get('src', '')[1:]
            file_type = 'js'

            if not path.exists():
                return elm
        
        else:
            file_type = 'css'

        with open(path, 'r') as file:
            content = file.read()

        if file_type == "css":
            content = self._minify_css(content)

        else:
            content = self._minify_js(content)

        name = self._get_name(file_type)

        new_path = Path(self._root) / '_cached' / file_type / f'{name}.{file_type}'
        new_path.parent.mkdir(parents=True, exist_ok=True)

        with open(new_path, 'w') as file:
            file.write(content)
        
        elm.set('href', f'/_cached/{file_type}/{name}.{file_type}')

        return elm
    
    def _minify_css(self, content) -> str:
        content = re.sub(r'/\*[\s\S]*?\*/', '', content)
        content = re.sub(r'\s*([{}:;,])\s*', r'\1', content)
        content = re.sub(r';\}', '}', content)
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r'\s*([>+~])\s*', r'\1', content)
        content = content.strip()
        
        return content
    
    def _register_functions(self):
        return
