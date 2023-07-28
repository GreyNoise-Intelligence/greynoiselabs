#!/usr/bin/env python
"""GreyNoise Labs API client package."""
import os

from setuptools import find_packages, setup


def read(fname):
    """Read file and return its contents."""
    with open(os.path.join(os.path.dirname(__file__), fname)) as input_file:
        return input_file.read()


setup(
    name="greynoiselabs",
    version="0.1.8",
    description="Abstraction to interact with GreyNoise Labs GraphQL API.",
    url="https://api.labs.greynoise.io/",
    author="GreyNoise Intelligence",
    author_email="labs@greynoise.io",
    license="MIT",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=read("requirements/common.txt").split("\n"),
    long_description=read("README.rst") + "\n\n" + read("CHANGELOG.md"),
    python_requires=">=3.0, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries",
    ],
    entry_points={"console_scripts": ["greynoiselabs = greynoiselabs.cli.main:app"]},
    zip_safe=False,
    keywords=["internet", "scanning", "threat intelligence", "security"],
    download_url="https://github.com/GreyNoise-Intelligence/greynoiselabs",
)
