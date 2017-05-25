
from setuptools import setup

version = open('VERSION.txt').read()

setup(name='storage',
        version=version,
        description='pytohn object storage',
        url='http://github.com/chuck1/storage',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=[
            'storage',
            'storage.filesystem'
            ],
        zip_safe=False,
        scripts=[
                'bin/web_sheets_storage',
                ],
            )

