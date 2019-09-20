#!/usr/bin/env python
from distutils.core import setup

INSTALL_REQUIRES = ["pyside2", "xlwt"]

PYTHON_REQUIRES = ">=3.5"

setup(
    name="nutrition",
    version="0.1",
    description="Healthy nutrition app",
    # url="https://github.com/TODO/TODO",
    packages=["nutrition"],
    install_requires=INSTALL_REQUIRES,
    python_requires=PYTHON_REQUIRES,
)
