import re

from docutils import nodes
from docutils.parsers.rst import roles


def awesome(name, rawtext, text, lineno, inliner, options={}, content=[]):
    html = '<span class="{text}"></span>'.format(text=text)
    return [nodes.raw('', html, format='html')], []


def awesome_link(name, rawtext, text, lineno, inliner, options={}, content=[]):
    cls, href, _ = re.split(" <|>", text)
    html = f'<a href="{href}" target="_blank"><span class="{cls}"></span></a>'
    return [nodes.raw('', html, format='html')], []



def register():
    roles.register_local_role('awesome', awesome)
    roles.register_local_role('awesome-link', awesome_link)
