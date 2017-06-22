import os
from setuptools import setup

import pkgtool

pkg = pkgtool.Package(os.getcwd())

setup(**pkg.setup_args())


