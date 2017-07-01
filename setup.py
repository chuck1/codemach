import os
import re
from setuptools import setup
import toml

with open('Pytool') as f:
    c = toml.loads(f.read())

with open(os.path.join(c['name'], '__init__.py')) as f:
    version = re.findall("^__version__ = '(.*)'", f.read())[0]

with open('requirements.txt') as f:
    install_requires=[l.strip() for l in f.readlines()]
    
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
        'setup_requires': ['toml']
        }

setup(**kwargs)



