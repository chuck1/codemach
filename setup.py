
from setuptools import setup

setup(name='web_sheets',
        version='0.1',
        description='python spreadsheets',
        url='http://github.com/chuck1/sheets',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=['sheets'],
        package_dir={'sheets':'sheets'},
        install_requires=[
            'fs',
            'numpy',
            ],
        zip_safe=False,
        )

