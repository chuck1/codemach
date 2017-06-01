
from setuptools import setup

version = open('VERSION.txt').read()

setup(name='ws_web_aiohttp',
        version=version,
        description='web server for web-sheets project',
        url='http://github.com/chuck1/web_sheets',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=[
            'ws_web_aiohttp',
            'ws_web_aiohttp.tests',
            'ws_web_aiohttp.tests.conf',
            'ws_web_aiohttp.static',
            'ws_web_aiohttp.templates',
            ],
        zip_safe=False,
        scripts=[
                #'bin/ws_web_aiohttp',
                ],
        package_data={'': [
            '*.service',
            '*.html',
            '*.js']},
        install_requires=[
            'aiohttp',
            'requests_oauthlib',
            'jinja2',
            'modconf',
            'ws_sheets_server',
            ]
            )

