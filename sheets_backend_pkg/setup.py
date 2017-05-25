
from setuptools import setup

version = open('VERSION.txt').read()

setup(name='sheets_backend',
        version=version,
        description='backends for managing sheets objects',
        url='http://github.com/chuck1/sheets_backend',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=[
            'sheets_backend',
            'sheets_backend.sockets',
            'sheets_backend.tests',
            ],
        zip_safe=False,
        scripts=[
                'bin/web_sheets_sheets_backend',
                ],
            )

