
from setuptools import setup

setup(name='web_sheets',
        version='0.1a11',
        description='python spreadsheets',
        url='http://github.com/chuck1/sheets',
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
            ],
        entry_points={
            'console_scripts':[
                'web_sheets_storage = storage.daemon:daemon',
                'web_sheets_sheets_backend = sheets_backend.daemon:daemon',
                ]
            },
        data_files=[
            ('/lib/systemd/system', [
                'daemon/web_sheets_storage.service',
                'daemon/web_sheets_sheets_backend.service',
                ]),
            ('/etc/web_sheets_storage/web_sheets_storage', [
                'daemon/web_sheets_storage/settings.py',
                'daemon/web_sheets_storage/__init__.py',
                ]),
            ('/etc/web_sheets_sheets_backend/web_sheets_sheets_backend', [
                'daemon/web_sheets_sheets_backend/__init__.py',
                'daemon/web_sheets_sheets_backend/settings.py',
                ]),
            ],
        zip_safe=False,
        )

