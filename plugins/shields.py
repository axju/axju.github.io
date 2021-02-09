import re

from docutils import nodes
from docutils.parsers.rst import roles

SHILDS_PYTHON = """
<a class="reference external image-reference" href="https://github.com/axju/{github}"><img alt="GitHub top language" src="https://img.shields.io/github/languages/top/axju/{github}" /></a>
<a class="reference external image-reference" href="https://github.com/axju/{github}"><img alt="Lines of code" src="https://img.shields.io/tokei/lines/github/axju/{github}" /></a>
<a class="reference external image-reference" href="https://pypi.org/project/{pypi}/"><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/{pypi}" /></a>
"""

SHILDS_JENKINS = """
<a class="reference external image-reference" href="https://jenkins.axju.de/job/axju/job/{jenkins}/"><img alt="Jenkins" src="https://img.shields.io/jenkins/build/https/jenkins.axju.de/job/axju/job/{jenkins}/job/master" /></a>
<a class="reference external image-reference" href="https://jenkins.axju.de/job/axju/job/{jenkins}/"><img alt="Jenkins Coverage" src="https://img.shields.io/jenkins/coverage/cobertura/https/jenkins.axju.de/job/axju/job/{jenkins}/job/master" /></a>
"""

def shields_full(name, rawtext, text, lineno, inliner, options={}, content=[]):
    values = text.split()
    github = values[0]
    pypi = values[1] if len(values) > 1 else values[0]
    html = (SHILDS_JENKINS + SHILDS_PYTHON + '<br>').format(github=github, pypi=pypi, jenkins=github)
    return [nodes.raw('', html, format='html')], []

def shields_python(name, rawtext, text, lineno, inliner, options={}, content=[]):
    values = text.split()
    github = values[0]
    pypi = values[1] if len(values) > 1 else values[0]
    html = (SHILDS_PYTHON + '<br>').format(github=github, pypi=pypi)
    return [nodes.raw('', html, format='html')], []

def shields_jenkins(name, rawtext, text, lineno, inliner, options={}, content=[]):
    html = (SHILDS_JENKINS + '<br>').format(jenkins=text)
    return [nodes.raw('', html, format='html')], []

def register():
    roles.register_local_role('shields-full', shields_full)
    roles.register_local_role('shields-python', shields_python)
    roles.register_local_role('shields-jenkins', shields_jenkins)
