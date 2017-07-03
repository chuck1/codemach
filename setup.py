import os
import re
import json
from setuptools import setup

with open('Setup.lock') as f:
    c = json.loads(f.read())

with open(os.path.join(c['name'], '__init__.py')) as f:
    version = re.findall("^__version__ = '(.*)'", f.read())[0]

with open('Pipfile.lock') as f:
    p = json.loads(f.read())
    install_requires=[k + v['version'] for k, v in p['default'].items()]

kwargs = {
        'name': c['name'],
        'version': version,
        'description': c['description'],
        'url': c['url'],
        'author': c['author'],
        'author_email': c['author_email'],
        'license': c['license'],
        'packages': c.get('packages', []),
        'zip_safe': False,
        'scripts': c.get('scripts',[]),
        'package_data': c.get('package_data',{}),
        'install_requires': install_requires,
        }

setup(**kwargs)



