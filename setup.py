#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import setuptools
import shutil
import sys

__title__ = "crossplane_update"
__summary__ = "Helper script for updating crossplane.analyzer.DIRECTIVES"
__url__ = "https://github.com/aluttik/crossplane_update"

__version__ = "0.0.0"

__author__ = "Arie van Luttikhuizen"
__email__ = "aluttik@gmail.com"

__license__ = "MIT"

here = os.path.abspath(os.path.dirname(__file__))


def get_readme():
    path = os.path.join(here, "README.md")
    with io.open(path, encoding="utf-8") as f:
        return "\n" + f.read()


setuptools.setup(
    name=__title__,
    version=__version__,
    description=__summary__,
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    author=__author__,
    author_email=__email__,
    url=__url__,
    packages=[],
    install_requires=["requests>=2.21.0", "bs4>=0.0.1"],
    license=__license__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["crossplane-update = crossplane_update:main"]},
)
