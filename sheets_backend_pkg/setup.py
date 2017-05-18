
from setuptools import setup

setup(name='sheets_backend',
        version='0.1',
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
        entry_points={
            'console_scripts':[
                'web_sheets_sheets_backend = sheets_backend.daemon:daemon'
                ]
            })

