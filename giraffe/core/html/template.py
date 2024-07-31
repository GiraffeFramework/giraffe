from typing import Optional

from lxml import etree

import re


TEMPLATE_REGEX = re.compile(r'{%\s*(\w+)\s*(.*?)\s*%}')


class Template:
    def __init__(self, template: str, is_file: bool=True):
        self._template: str = ""

        if is_file:
            with open(template, 'r') as file:
                self._template = file.read()
            
            self._parse()

        else:
            self._template = template

    def _parse(self) -> None:
        root = etree.HTML(self._template, None)

        self._process_attributes(root)
        self._process_template_tags(etree.tostring(root, encoding='unicode')) # type: ignore

    def _process_attributes(self, root) -> None:
        for elm in root.iter():
            grf_attrs = {k: elm for k, v in elm.attrib.items() if k.startswith('grf-')}

            print(grf_attrs)

    def _process_template_tags(self, content):
        def replace_tag(match):
            func_name, args = match.groups()
            
            print(func_name, args)

            return f"PROCESSED_{func_name}({args})"

        self._template = TEMPLATE_REGEX.sub(replace_tag, content)

    def substitute(self, context: Optional[dict]) -> str:
        if not context:
            return self._template
        
        return self._template
