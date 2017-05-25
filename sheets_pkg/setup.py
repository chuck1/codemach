import os
from setuptools import setup

version = open('VERSION.txt').read()

setup(name='sheets',
        version=version,
        description='python spreadsheets',
        url='http://github.com/chuck1/sheets',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=[
            'sheets',
            'sheets.tests',
            'sheets.ext.middleware',
            ],
        install_requires=[
            'fs',
            'numpy',
            ],
        zip_safe=False,
        )

