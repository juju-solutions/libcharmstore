#!/usr/bin/env python
#
# Copyright 2013 Marco Ceppi.  This software is licensed under the
# GNU General Public License version 3 (see the file LICENSE).

import ez_setup


ez_setup.use_setuptools()

from setuptools import setup


setup(
    name='charmworldlib',
    version="0.2.4-1",
    packages=['charmworldlib'],
    maintainer='Marco Ceppi',
    maintainer_email='marco@ceppi.net',
    description=('Library to access charmworld data'),
    license='GPL v3',
    url='https://launchpad.net/charmworldlib',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
