
from setuptools import setup

setup(name='web_sheets',
        version='0.1a1',
        description='python spreadsheets',
        url='http://github.com/chuck1/sheets',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=[
            'storage',
            'sheets',
            'sheets_backend'],
        package_dir={
            'storage':'storage_pkg/storage',
            'sheets':'sheets_pkg/sheets',
            'sheets_backend':'sheets_backend_pkg/sheets_backend',
            },
        install_requires=[
            'fs',
            'numpy',
            ],
        zip_safe=False,
        )

