#!/usr/bin/env python3

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "pyload_utils",
    version = "0.1.0",
    author = "Thammi",
    author_email = "thammi@chaossource.net",
    description = ("Some usefull utilities for the pyload download manager"),
    license = "GPLv3",
    keywords = "pyload",
    packages=['pyloadutils'],
    long_description=read('README.md'),
    classifiers=[
    ],
    entry_points={
        'console_scripts': [
            'pyload_merge = pyloadutils.merger:main',
            'pyload_restart = pyloadutils.restart:main',
            'pyload_deloffline = pyloadutils.deloffline:main',
            'pyload_del404 = pyloadutils.del_404:main',
            'pyload_checkincomplete = pyloadutils.check_incomplete:main',
            ],
        },
)

