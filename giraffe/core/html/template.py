from typing import Optional

from lxml import etree

from .attributes import AttributeFunctions

import re


TEMPLATE_TAG_REGEX = re.compile(r'{%\s*(\w+)\s*(.*?)\s*%}')


class Template:
    def __init__(self, template: str, is_file: bool=True, root: str=""):
        self._template: str = ""
        self._root: str = root

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
            elm: etree._Element

            for attribute in elm.attrib.keys():
                if not attribute.startswith('grf-'):
                    continue

                new_elm = AttributeFunctions(self._root).functions[attribute](elm)

                parent = new_elm.getparent()

                if parent is not None:
                    parent.replace(elm, new_elm)

                    continue

                else:
                    raise AttributeError("Wrong attribute.")

    def _process_template_tags(self, content):
        def replace_tag(match):
            func_name, args = match.groups()
            
            #print(func_name, args)

            return f"PROCESSED_{func_name}({args})"

        self._template = TEMPLATE_TAG_REGEX.sub(replace_tag, content)

    def substitute(self, context: Optional[dict]) -> str:
        if not context:
            return self._template
        
        return self._template
