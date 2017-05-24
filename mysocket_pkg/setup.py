
from setuptools import setup

version = open('VERSION.txt').read()

setup(name='mysocket',
        version=version,
        description='convenient wrapper for python socket',
        url='http://github.com/chuck1/mysocket',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=['mysocket'],
        zip_safe=False,
        )

