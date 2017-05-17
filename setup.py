
from setuptools import setup

setup(name='web_sheets',
        version='0.1a0',
        description='python spreadsheets',
        url='http://github.com/chuck1/sheets',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=['storage','sheets'],
        package_dir={
            'sheets':'sheets_pkg/sheets',
            'storage':'storage_pkg/storage'},
        install_requires=[
            'fs',
            'numpy',
            ],
        zip_safe=False,
        )

