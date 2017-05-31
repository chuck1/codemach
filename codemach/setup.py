
from setuptools import setup

version = open('VERSION.txt').read()

setup(name='codemach',
        version=version,
        description='very simple tool for executing python code objects',
        url='http://github.com/chuck1/codemach',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=[
            'codemach',
            'codemach.tests',
            ],
        zip_safe=False,
        )

