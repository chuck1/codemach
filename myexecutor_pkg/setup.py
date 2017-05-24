
from setuptools import setup

version = open('VERSION.txt').read()

setup(name='myexecutor',
        version=version,
        description='very simple tool for executing python code objects',
        url='http://github.com/chuck1/myexecutor',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=['myexecutor'],
        zip_safe=False,
        )

