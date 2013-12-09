#!/usr/bin/env python
#
# Copyright 2013 Marco Ceppi.  This software is licensed under the
# GNU General Public License version 3 (see the file LICENSE).

import sys
import ez_setup


ez_setup.use_setuptools()

from charmworldlib.version import __VERSION__
from setuptools import setup, find_packages


setup(
    name='charmworldlib',
    version=__VERSION__,
    packages=['charmworldlib'],
    install_requires=['requests', 'pyyaml'],
    maintainer='Marco Ceppi',
    maintainer_email='marco@ceppi.net',
    description=('Library to access charmworld data'),
    license='GPL v3',
    url='https://launchpad.net/charmworldlib',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
    ],
)
