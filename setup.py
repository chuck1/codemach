
from setuptools import setup

version = open('VERSION.txt').read()

setup(name='web_sheets',
        version=version,
        description='python web spreadsheets',
        url='http://github.com/chuck1/web_sheets',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=[
            'mysocket',
            'storage',
            'storage.filesystem',
            'sheets',
            'sheets.tests',
            'sheets_backend',
            'sheets_backend.sockets',
            'sheets_backend.tests',
            ],
        package_dir={
            'mysocket':'mysocket_pkg/mysocket',
            'storage':'storage_pkg/storage',
            'sheets':'sheets_pkg/sheets',
            'sheets_backend':'sheets_backend_pkg/sheets_backend',
            },
        install_requires=[
            'fs',
            'numpy',
            'django',
            #'social_django',
            'social-auth-app-django',
            'selenium',
            ],
        scripts=[
                'storage_pkg/bin/web_sheets_storage',
                'sheets_backend_pkg/bin/web_sheets_sheets_backend',
                ],
        zip_safe=False,
        )

