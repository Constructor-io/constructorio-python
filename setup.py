#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

VERSION = "0.0.12"


setup(
    name="constructor-io",
    version=VERSION,
    download_url='https://github.com/Constructor-io/constructorio-python'
                 '/tarball/' + VERSION,
    license="MIT",
    description="Constructor.IO Python Client",
    author="Constructor.io",
    author_email="info@constructor.io",
    url="https://www.constructor.io",
    install_requires=[
        'requests~=2.26'
    ],
    packages=["constructor_io"],
)
