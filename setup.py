
from setuptools import setup

setup(name='storage',
        version='0.1',
        description='pytohn object storage',
        url='http://github.com/chuck1/storage',
        author='Charles Rymal',
        author_email='charlesrymal@gmail.com',
        license='MIT',
        packages=['storage'],
        zip_safe=False,
        entry_points={
            'console_scripts':[
                'web_sheets_storage = storage.daemon'
                ]
            })

