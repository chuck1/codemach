#!/usr/bin/env python

import os

from distutils.core import setup
#from setuptools import setup, find_packages

template_files = list(
        os.path.join('templates',x) for x in os.listdir('templates'))

setup(
    name=           'python_spreadsheet',
    version=        '1.1',
    description=    'Python Spreadsheet Web App',
    author=         'Charles Rymal',
    author_email=   'charlesrymal@gmail.com',
    url=            'https://www.github.com/chuck1/python-spreadsheet/',
    packages=['python_spreadsheet'],
    #package_data={'python_resume':['templates/*']},
    data_files=[
        ('python_spreadsheet/templates', template_files),
            ],
    )

