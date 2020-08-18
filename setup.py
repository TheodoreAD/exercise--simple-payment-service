#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os.path import basename, dirname, join, splitext

from setuptools import find_packages, setup


def read(*path_tokens: str, encoding: str = "utf-8") -> str:
    with open(join(dirname(__file__), *path_tokens), encoding=encoding) as f:
        return f.read()


SOURCES_ROOT = "src"

setup(
    name="simple_payment_service",
    version="0.1",
    description="Python Flask service as an exercise",
    long_description=read("README.md"),
    author="Teodor Dumitrescu",
    author_email="teodor.dumitrescu@gmail.com",
    url="https://github.com/TheodoreAD/exercise--simple-payment-service",
    packages=find_packages(SOURCES_ROOT),
    package_dir={"": SOURCES_ROOT},
    py_modules=[splitext(basename(path))[0] for path in glob(f"{SOURCES_ROOT}/*.py")],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[read("requirements.txt").splitlines()],
    entry_points={
        "console_scripts": [
            "simple_payment_service=simple_payment_service.api:start_app",
            "simple_payment_service_dev=simple_payment_service.api:start_app_dev",
        ]
    },
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Utilities",
    ],
)
