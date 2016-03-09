#!/usr/bin/env python
#
# Copyright 2016 Marco Ceppi.  This software is licensed under the
# GNU Library or Lesser General Public License.

from setuptools import setup


setup(
    name='libcharmstore',
    version="0.0.1",
    packages=['charmstore'],
    maintainer='Marco Ceppi',
    maintainer_email='marco@ceppi.net',
    description=('Library to access charmstore data'),
    license='LGPL',
    url='https://github.com/juju-solutions/libcharmstore',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    ],
)
