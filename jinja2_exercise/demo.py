#! coding: utf-8

from jinja2 import Template
from pprint import pprint

if __name__ == '__main__':
    template = Template('Hello {{ name }}!')
    template.render(name='John Doe')

    pprint(template)