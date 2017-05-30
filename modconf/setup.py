
from setuptools import setup

version = open('VERSION.txt').read()

setup(name='modconf',
        version=version,
        description='pattern for loading configuration files that are python code',
        url='http://github.com/chuck1/web_sheets',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=['modconf'],
        zip_safe=False,
        )

